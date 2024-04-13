from django.db import models
import string
import random

def generate_unique_code():
    length = 6

    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Quiz.objects.filter(code=code).count() == 0:
            break
    return code

def create_quiz(user, popularity=5, danceability=5, energy=5, valence=5, tempo=80, title='', description=''):
    code = generate_unique_code()
    return Quiz.objects.create(
        code=code,
        user=user,
        popularity=popularity,
        danceability=danceability,
        energy=energy,
        valence=valence,
        tempo=tempo,
        title=title,
        description=description
    )

# Create your models here.
class Quiz(models.Model):
    code = models.CharField(max_length=8, default=generate_unique_code, unique=True)
    user = models.CharField(max_length=50, unique=True)
    popularity = models.IntegerField(null=False, default = 5)
    danceability = models.IntegerField(null=False, default = 5)
    energy = models.IntegerField(null=False, default = 5)
    valence = models.IntegerField(null=False, default = 5)
    tempo = models.IntegerField(null=False, default = 80)
    created_at = models.DateTimeField(auto_now_add=True)

