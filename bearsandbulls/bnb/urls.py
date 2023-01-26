from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('login/', views.login_view, name="login"),
    path('rules/', views.rules, name="rules"),
    path('pregame/', views.pregame, name="pregame"),
    path('game/', views.game_view, name="game"),
    path('endgame/', views.endgame, name="endgame"),
]

urlpatterns += staticfiles_urlpatterns()
