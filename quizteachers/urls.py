from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.home, name = 'quiz-home'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('create-quiz/', views.create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
]