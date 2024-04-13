from django.urls import path 
from .views import index

app_name = 'frontend'

urlpatterns = [
    path('', index, name=''),
    path('quiz/', index),
    path('quiz', index),
    path('recc/<str:quizCode>', index, name='recc')
]