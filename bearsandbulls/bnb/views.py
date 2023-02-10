import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from .models import game, word, gamelog


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(username=username, email=email, password=password, )
        user.save();
        messages.success(request, "Your account has been successfully created")
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username1 = request.POST['username1']
        password1 = request.POST['password1']
        user1 = authenticate(username=username1, password=password1)

        if user1 is not None:
            login(request, user1)

            return render(request, "rules.html")

        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "register.html")
    return render(request, 'register.html')


@login_required
def rules(request):
    player_id = request.user
    print(f"player is {player_id},{player_id.id}")
    return render(request, 'rules.html')


@login_required
def pregame(request):
    if request.method == 'POST':
        request.session['display'] = ""
        request.session['rough'] = ""
        request.session['turn'] = 0
        player = request.user
        playerch = request.POST['player']
        opp_game_id = str(request.POST['txtvalue']).strip()
        print(f"game_id {request.user.id}")
        if opp_game_id != "":
            game_obj2 = game.objects.filter(game_id=opp_game_id).first()
            game_obj2.opponent_id = request.user.id
            game_obj2.is_active = 1
            game_obj2.save()
            game_id = game_obj2.game_id
        else:
            difficulty = request.POST['difficulty']
            length = request.POST['length']
            game_id = increment_game_number()
            if player is not None:
                game_obj = game()
                game_obj.game_id = game_id
                game_obj.player_id = player.id
                if playerch == 'single':
                    game_obj.is_active = 1
                game_obj.player_mode = playerch
                game_obj.difficulty = difficulty
                game_obj.word_length = length
                swfilter = word.objects.filter(length=length).filter(difficulty=difficulty)
                game_obj.word = random.choice(list(swfilter.values()))['word_id']
                game_obj.save()
        request.session['game_id'] = game_id
        request.session['gamelog_id'] = game_id
        gamelogobj = gamelog()
        gamelogobj.gamelog_id = game_id
        gamelogobj.save()
        return render(request, 'game.html')
    return render(request, 'pregame.html')


def bears_and_bulls(superword, curword, game_id, request, description, phonetic):
    message = ""
    input_word = curword.upper()
    super_word = superword.upper()
    print(input_word + " " + super_word)
    invalid = False

    if len(input_word) != len(super_word):
        message = f"Please enter a {len(super_word)} lettered word..."
        invalid = True
    else:
        for i in range(len(super_word)):
            for j in range(i + 1, len(super_word)):
                if input_word[i] == input_word[j]:
                    invalid = True
        if invalid:
            message = "Cannot accept word with duplicate letters, please enter new word..."

    if not invalid:
        bears = 0
        bulls = 0
        for i in range(len(super_word)):
            for j in range(len(super_word)):
                if (input_word[i] == super_word[j]) and (i == j):
                    bulls += 1
                elif (input_word[i] == super_word[j]) and (i != j):
                    bears += 1

        if bulls == len(super_word):
            message = f"Congratulations you have guessed the word correct ! The word was {super_word}. Description: {description} Phonetic:{phonetic}"
            gameobj = game.objects.filter(game_id=game_id).first()
            gameobj.is_active = 2
            gameobj.winner = request.user.id
            gameobj.save()
        else:
            message = f"YOUR WORD - {input_word} - {str(bears)} BEARS AND {str(bulls)}  BULLS."

    return message


@login_required
def game_view(request):
    gamelog_id = request.session['gamelog_id']
    print(f"game log id {gamelog_id}")
    gamelogobj = gamelog.objects.all().filter(gamelog_id=gamelog_id).first()
    gameid = request.session['game_id']
    gameobj = game.objects.filter(game_id=gameid).first()
    if gameobj.is_active == 0:
        messages.info(request, "Wait for your opponent to join...")
    if gameobj.is_active == 1:
        if request.method == 'POST':
            current_word = request.POST['text']
            gamelogobj.inputtext = current_word
            wrd = word.objects.filter(word_id=gameobj.word).first()
            message = bears_and_bulls(wrd.word, current_word, gameid,
                                      request, wrd.description, wrd.phonetic)
            if "Congratulations" in message:
                messages.success(request,
                                 f"You have guessed the word correct ! The word was {wrd.word.upper()}."
                                 f" Description: {wrd.description} "
                                 f"Phonetic: {wrd.phonetic}")
            display = request.user.username + ": " + message + "\n" + gamelogobj.display
            request.session['turn'] = display.count(request.user.username)
            gamelogobj.rough = request.POST['rough']
            gamelogobj.display = display
            request.session['display'] = display
            request.session['rough'] = request.POST['rough']
            gamelogobj.save()
    return render(request, 'game.html')


def openPopup(request):
    if "Congratulations" in message:
        return render(request, 'game.html', {"bnb": message})


def endgame(request):
    return render(request, 'endgame.html')


def increment_game_number():
    gids = game.objects.all().values_list('game_id', flat=True)
    last_game = []
    if not gids:
        return 'BNB_' + '0'
    for i in gids:
        last_game.append(int(i.split('_')[1]))
    last_game.sort()
    booking_int = last_game[len(last_game) - 1] + 1
    return 'BNB_' + str(booking_int)


def logout_view(request):
    logout(request)
    return render(request,'register.html')
