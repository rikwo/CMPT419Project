from rest_framework import serializers
from .models import Quiz

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('id', 'code', 'user', 'popularity', 'danceability', 'energy', 'valence', 'tempo', 'created_at')

class CreateQuizResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('popularity', 'danceability', 'energy', 'valence', 'tempo')