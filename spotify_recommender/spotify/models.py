from django.db import models

class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=150)
    access_token = models.CharField(max_length=150)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)

class Playlist(models.Model):

    playlist_id = models.CharField(max_length=120, primary_key=True)
    playlist_name = models.TextField(max_length=100)
    playlist_url = models.CharField(max_length=1000)
    playlist_num_tracks = models.IntegerField(null=True)
    playlist_featured = models.BooleanField(default=False)
    playlist_owner = models.CharField(max_length=500)
    date_created = models.CharField(max_length=500, default="No date")
    playlist_img_src = models.CharField(max_length=5000, null=True, default="no_img")

    def __str__(self):
        return self.playlist_name