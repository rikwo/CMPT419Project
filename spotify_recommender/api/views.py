from django.shortcuts import render
from rest_framework import generics, status
from .serializers import QuizSerializer, CreateQuizResultSerializer
from .models import Quiz
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from django.http import JsonResponse
from spotify.models import SpotifyToken
from spotify.utils import get_user_tokens
from django.views.decorators.http import require_GET
from ml.pipeline import recommend_top_songs_and_create_playlist 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotify.credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

# Create your views here.
class QuizView(generics.CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class GetQuiz(APIView):
    serializer_class = QuizSerializer
    lookup_url_kwarg = 'code'

    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            quiz = Quiz.objects.filter(code=code)
            if len(quiz) > 0:
                data = QuizSerializer(quiz[0]).data
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Results Not Found': 'Invalid Quiz Code'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request': 'Code parameter not found in request'}, status=status.HTTP_400_BAD_REQUEST)

class CreateQuizView(APIView):
    serializer_class = CreateQuizResultSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            popularity = serializer.data.get('popularity')
            danceability = serializer.data.get('danceability')
            energy = serializer.data.get('energy')
            valence = serializer.data.get('valence')
            tempo = serializer.data.get('tempo')
            user = self.request.session.session_key
            queryset = Quiz.objects.filter(user=user)
            if queryset.exists():
                quiz = queryset[0]
                quiz.popularity = popularity
                quiz.danceability = danceability
                quiz.energy = energy
                quiz.valence = valence
                quiz.tempo = tempo
                quiz.save(update_fields=['popularity', 'danceability', 'energy', 'valence', 'tempo'])
                self.request.session['quiz_code'] = quiz.code
                return Response(QuizSerializer(quiz).data, status=status.HTTP_200_OK)
            else:
                quiz = Quiz(user=user, popularity=popularity, danceability=danceability, energy=energy, valence=valence, tempo=tempo)
                quiz.save()
                self.request.session['quiz_code'] = quiz.code
                return Response(QuizSerializer(quiz).data, status=status.HTTP_201_CREATED)

        return Response(QuizSerializer(quiz).data, status=status.HTTP_201_CREATED)
    
@api_view(['GET'])
def user_in_quiz(request, format=None):
    if not request.session.exists(request.session.session_key):
        request.session.create()

    data = {
        'code': request.session.get('quiz_code')
    }
    return JsonResponse(data, status=status.HTTP_200_OK)
        
@api_view(['POST'])
def leave_quiz(request, format=None):
    if 'quiz_code' in request.session:
        request.session.pop('quiz_code')
        user = request.session.session_key
        quiz_results = Quiz.objects.filter(user=user)
        if quiz_results.exists():
            quiz = quiz_results.first()
            quiz.delete()

    return Response({'Message': 'Success'}, status=status.HTTP_200_OK)

@require_GET
def recommend_top_songs_view(request):
    quiz_code = request.GET.get('quizCode')
    if not quiz_code:
        return JsonResponse({"error": "Missing quizCode parameter"}, status=400)
    
    token = get_user_tokens(request.session.session_key)
    
    sp = spotipy.Spotify(auth=token.access_token)

    user = sp.user
    # Call your recommendation function to get recommended songs based on quiz code
    recommended_songs = recommend_top_songs_and_create_playlist(user, token.access_token, sp)

    return JsonResponse({"recommended_songs": recommended_songs})