from django.urls import path
from .views import QuizView, CreateQuizView, GetQuiz, user_in_quiz, leave_quiz, recommend_top_songs_view

urlpatterns = [
    path('quiz', QuizView.as_view()),
    path('create-quiz', CreateQuizView.as_view()),
    path('get-quiz', GetQuiz.as_view()),
    path('user-in-quiz', user_in_quiz),
    path('leave-quiz', leave_quiz),
    path('recommend-top-songs/', recommend_top_songs_view, name='recommend_top_songs'),
]