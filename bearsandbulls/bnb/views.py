from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):
    print("Inside register")
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(username=username, email=email, password=password, )
        user.save();
        messages.success(request, "Your account has been successfully created")
    return render(request, 'register.html')


def login(request):
    print("Inside login")
    if request.method == 'POST':
        username1 = request.POST['username1']
        password1 = request.POST['password1']
        print(f"username1{username1} password1{password1}")
        user1 = authenticate(username=username1, password=password1)

        if user1 is not None:
            return render(request, "rules.html")
        else:
            return render(request, "register.html", {"error": "Invalid username or password."})
    return render(request, 'register.html')


def rules(request):
    return render(request, 'rules.html')


def pregame(request):
    return render(request, 'pregame.html')


def game(request):
    return render(request, 'game.html')


def endgame(request):
    return render(request, 'endgame.html')
