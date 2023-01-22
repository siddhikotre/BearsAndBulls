from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('rules/', views.rules, name="rules"),
    path('pregame/', views.pregame, name="pregame"),
    path('game/', views.game, name="game"),
    path('endgame/', views.endgame, name="endgame"),
]
