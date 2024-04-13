from django.shortcuts import redirect
from .credentials import REDIRECT_URI, CLIENT_SECRET, CLIENT_ID
from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from requests import Request, post
from .utils import *
from api.models import Quiz
from .models import SpotifyToken
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from rest_framework.views import APIView

@api_view(['GET'])
def auth_url(request, format=None):
    scopes = 'user-library-read'

    url = Request('GET', 'https://accounts.spotify.com/authorize', params={
        'scope': scopes,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID
    }).prepare().url

    return Response({'url': url}, status=status.HTTP_200_OK)


@api_view(['GET'])
def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    
    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_user_tokens(
        request.session.session_key, access_token, token_type, expires_in, refresh_token)

    return redirect('frontend:')  # Assuming 'frontend:' is a valid URL name


@api_view(['GET'])
def is_authenticated(request, format=None):
    is_authenticated = is_spotify_authenticated(request.session.session_key)
    return Response({'status': is_authenticated}, status=status.HTTP_200_OK)

class SavedTracks(APIView):

    def get_artist_info(self, artist_id):
        # Define Spotify API endpoint for retrieving artist information
        endpoint = f"artists/{artist_id}"
        
        # Make a GET request to the Spotify API endpoint using internal function
        response = execute_spotify_api_request(None, endpoint)
        
        if response and 'genres' in response:
            return response

    def get(self, request, format=None):
        quiz_code = self.request.session.get('quiz_code')
        quiz = Quiz.objects.filter(code=quiz_code)[0]
        endpoint = "tracks/"
        response = execute_spotify_api_request(request.session.session_key, endpoint)
        if 'items' in response:
                tracks = response['items']
                
                if not tracks:
                    return Response({'error': 'No tracks found'}, status=status.HTTP_404_NOT_FOUND)
                
                # Prepare a list to store track information
                items = []
                
                for track in tracks:
                    # Extract desired track information
                    item = {
                        'name': track['track']['name'],
                        'artist': track['track']['artists'][0]['name'],
                        'album': track['track']['album']['name'],
                        'duration_ms': track['track']['duration_ms'],
                        'album_cover': track['track']['album']['images'][2]['url'],
                        'song_id': track['track']['id']
                    }
                    
                    # Append the item to the list
                    items.append(item)
                
                return Response(items, status=status.HTTP_200_OK)
            
        else:
            return Response({'error': 'Failed to retrieve tracks'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

