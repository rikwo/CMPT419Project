from django.urls import path
from . import views

urlpatterns = [
    path('get-auth-url', views.auth_url, name='get_auth_url'),
    path('redirect', views.spotify_callback),
    path('is-authenticated/', views.is_authenticated, name='is_authenticated'),
    path('tracks', views.SavedTracks.as_view())
]