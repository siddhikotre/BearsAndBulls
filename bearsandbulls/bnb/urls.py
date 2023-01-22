from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('rules/', views.rules, name="rules"),
    path('pregame/', views.pregame, name="pregame"),
]
