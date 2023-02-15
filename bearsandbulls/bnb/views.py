"""==========================#
Author : Siddhi Santosh Kotre
Project : Bears And Bulls
TYBSc IT Roll Number : 730
#=========================="""

# Importing packages
import random
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.shortcuts import render
from .models import game, word, gamelog, leaderboard


def index(request):
    return render(request, 'index.html')


# Module for registering a new user
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(username=username, email=email, password=password, )
        user.save();
        messages.success(request, "Your account has been successfully created")
    return render(request, 'register.html')


# Module for user login authentication
def login_view(request):
    # Retrieving user inputs for logging in
    if request.method == 'POST':
        username1 = request.POST['username1']
        password1 = request.POST['password1']
        user1 = authenticate(username=username1, password=password1)

        # Checking if user is valid and logging him into the game
        if user1 is not None:
            login(request, user1)
            return render(request, "rules.html")
        # if user is invalid displaying appropriate error message
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "register.html")
    return render(request, 'register.html')


# Rendering rules webpage
@login_required
def rules(request):
    player_id = request.user
    print(f"player is {player_id},{player_id.id}")
    return render(request, 'rules.html')


# Module for pre game setting selections
@login_required
def pregame(request):
    if request.method == 'POST':
        # Resetting the sessions for new game
        request.session['display'] = ""
        request.session['rough'] = ""
        request.session['turn'] = 0
        player = request.user
        playerch = request.POST['player']
        opp_game_id = str(request.POST['txtvalue']).strip()

        # If trying to join a duo game setting its id as opponent player id
        if opp_game_id != "":
            game_obj2 = game.objects.filter(game_id=opp_game_id).first()
            if game_obj2 is None or game_obj2.is_active!=0:
                messages.error(request,"Sorry, No such game exists! Please try again")
                return render(request, 'pregame.html')
            game_obj2.opponent_id = request.user.id
            game_obj2.is_active = 1
            game_obj2.save()
            game_id = game_obj2.game_id
        # Else, saving player's choice of length and difficulty of word
        else:
            difficulty = request.POST['difficulty']
            length = request.POST['length']
            # Generating a new Game ID using Increment Game Number method
            game_id = increment_game_number()

            if player is not None:
                game_obj = game()
                game_obj.game_id = game_id
                game_obj.player_id = player.id
                # If it is single player choice set game as active
                if playerch == 'single':
                    game_obj.is_active = 1
                game_obj.player_mode = playerch
                game_obj.difficulty = difficulty
                game_obj.word_length = length
                # Selecting a random super word based on player's choices
                swfilter = word.objects.filter(length=length).filter(difficulty=difficulty)
                game_obj.word = random.choice(list(swfilter.values()))['word_id']
                game_obj.save()
        # Setting game id as necessary sessions to be used during games
        request.session['game_id'] = game_id
        request.session['gamelog_id'] = game_id
        gamelogobj = gamelog()
        gamelogobj.gamelog_id = game_id
        gamelogobj.save()
        return render(request, 'game.html')
    return render(request, 'pregame.html')


# Core logic for calculating bears and bulls
def bears_and_bulls(superword, curword, game_id, request, description, phonetic):
    # Initializing variables and converting them into upper case for handling case sensitivity
    message = ""
    input_word = curword.upper()
    super_word = superword.upper()
    print(input_word + " " + super_word)
    invalid = False

    # Input word validation block
    # Rule : The input word length should be same as the length selected in pre game settings.
    if len(input_word) != len(super_word):
        message = f"Please enter a {len(super_word)} lettered word..."
        invalid = True
    else:
        # Rule : Letters in the word should not be repeated.
        for i in range(len(super_word)):
            for j in range(i + 1, len(super_word)):
                if input_word[i] == input_word[j]:
                    invalid = True
        # If any of the above rule is not satisfied set appropriate error message
        if invalid:
            message = "Cannot accept word with duplicate letters, please enter new word..."
    # If the entered word is valid, calculating bears and bulls
    if not invalid:
        bears = 0
        bulls = 0
        for i in range(len(super_word)):
            for j in range(len(super_word)):
                if (input_word[i] == super_word[j]) and (i == j):
                    bulls += 1
                elif (input_word[i] == super_word[j]) and (i != j):
                    bears += 1

        # If number of bulls is equal to length of superword you have won the game
        if bulls == len(super_word):
            message = f"Congratulations you have guessed the word correct ! The word was {super_word}. Description: {description} Phonetic:{phonetic}"
            gameobj = game.objects.filter(game_id=game_id).first()
            gameobj.is_active = 2
            # Setting respective player scores
            if request.user.id == gameobj.player_id:
                gameobj.p1_score = int(request.session['turn']) + 1
            elif request.user.id == gameobj.opponent_id:
                gameobj.p2_score = int(request.session['turn']) + 1
            gameobj.winner = request.user.id
            gameobj.save()
        # If the game is not over displaying number of bears and bulls
        else:
            message = f"YOUR WORD - {input_word} - {str(bears)} BEARS AND {str(bulls)}  BULLS."

    return message


@login_required
def game_view(request):
    # Retrieving game session details
    gamelog_id = request.session['gamelog_id']
    print(f"game log id {gamelog_id}")
    gamelogobj = gamelog.objects.all().filter(gamelog_id=gamelog_id).first()
    gameid = request.session['game_id']
    gameobj = game.objects.filter(game_id=gameid).first()
    # If the player has selected duo mode, game does not start if opponent has not joined
    if gameobj.is_active == 0:
        messages.info(request, "Wait for your opponent to join...")
    gameid = request.session['game_id']
    gameobj = game.objects.filter(game_id=gameid).first()
    wrd = word.objects.filter(word_id=gameobj.word).first()
    # Terminating the game if the opponent has already won
    if gameobj.is_active == 2:
        messages.info(request,
                      f"Your opponent won the game, The word was {wrd.word} which means {wrd.description} and it is pronounced as {wrd.phonetic}. Try again next time...")
        # Saving the current scores of the player
        if request.user.id == gameobj.player_id:
            gameobj.p1_score = int(request.session['turn']) + 1
        elif request.user.id == gameobj.opponent_id:
            gameobj.p2_score = int(request.session['turn']) + 1
        gameobj.save()
        return render(request, 'endgame.html')
    # Terminating if your opponent quits the game
    if gameobj.is_active == 3:
        messages.info(request,
                      f"Unfortunately your opponent quit the game. The word was {wrd.word} which means {wrd.description} and it is pronounced as {wrd.phonetic}. Please join a new game.")
        return render(request, 'endgame.html')
    # Main active game logic
    if gameobj.is_active == 1:
        if request.method == 'POST':
            current_word = request.POST['text']
            gamelogobj.inputtext = current_word
            wrd = word.objects.filter(word_id=gameobj.word).first()
            # Passing the input value from players to Bears and Bulls Method
            message = bears_and_bulls(wrd.word, current_word, gameid,
                                      request, wrd.description, wrd.phonetic)
            if "Congratulations" in message:
                messages.success(request,
                                 f"You have guessed the word correct ! The word was {wrd.word.upper()}."
                                 f" Description: {wrd.description} "
                                 f"Phonetic: {wrd.phonetic}")

                # Setting leaderboard values
                leader_row = leaderboard.objects.filter(word_length=gameobj.word_length).filter(
                    difficulty=gameobj.difficulty).first()
                # If this is the first entry in that leaderboard category
                if not leader_row.num_of_turns.isnumeric():
                    leader_row.player_id = request.user.id
                    leader_row.user_name = request.user.username
                    leader_row.num_of_turns = int(request.session['turn']) + 1
                    leader_row.save()
                # If it is not the first entry comparing the existing high scores
                elif int(request.session['turn']) < int(leader_row.num_of_turns):
                    leader_row.player_id = request.user.id
                    leader_row.user_name = request.user.username
                    leader_row.num_of_turns = int(request.session['turn']) + 1
                    leader_row.save()
                return render(request, 'endgame.html')

            # Display area updated with the latest message
            display = request.user.username + ": " + message + "\n" + gamelogobj.display
            request.session['turn'] = display.count(request.user.username)
            gamelogobj.rough = request.POST['rough']
            gamelogobj.display = display
            request.session['display'] = display
            request.session['rough'] = request.POST['rough']
            gamelogobj.save()
    return render(request, 'game.html')


# Rendering end game page
def endgame(request):
    return render(request, 'endgame.html')


# Module for quit game event
def quit_event(request):
    gameid = request.session['game_id']
    gameobj = game.objects.filter(game_id=gameid).first()
    # Setting game active id as 3, to notify opponent that other player has quit the game.
    gameobj.is_active = 3
    gameobj.save()
    wrd = word.objects.filter(word_id=gameobj.word).first()
    # Displaying the superword to the player
    messages.info(request,
                  f"Better Luck Next Time! The word was {wrd.word} which means {wrd.description} and it is pronounced as {wrd.phonetic}.")
    return render(request, 'endgame.html')


# Module for generating new game ID
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


# Displaying leaderboard on the page
def leaderboard_view(request):
    data = serializers.serialize("python", leaderboard.objects.all())
    context = {
        'data': data,
    }
    return render(request, 'leaderboard.html', context)


# Module for a player to log out of current session
def logout_view(request):
    logout(request)
    return render(request, 'register.html')
