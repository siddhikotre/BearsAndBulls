from django.db import models


class word(models.Model):
    word_id = models.IntegerField(primary_key=True)
    word = models.CharField(max_length=50)
    length = models.IntegerField(default=4)
    difficulty = models.CharField(max_length=20, default="easy")
    description = models.CharField(max_length=200, default="Description not available")
    phonetic = models.CharField(max_length=200, default="phonetic not available")

    def __str__(self):
        return self.name


'''=================================================================================
game.is_active options:
game.is_active = 0 -> The game is inactive and waiting for your opponent to join
game.is_active = 1 -> The game is active and in play
game.is_active = 2 -> The game is inactive since your opponent has won the game
game.is_active = 3 -> The game is inactive since your opponent has quit the game
=================================================================================='''


class game(models.Model):
    player_id = models.IntegerField()
    game_id = models.CharField(primary_key=True, max_length=50)
    opponent_id = models.IntegerField(default=0)
    is_active = models.IntegerField(default=0)
    game_date = models.DateField(auto_now=True)
    player_mode = models.CharField(max_length=20, default='single')
    word_length = models.IntegerField(default=4)
    difficulty = models.CharField(max_length=20, default='easy')
    word = models.IntegerField()
    p1_score = models.IntegerField(default=0)
    p2_score = models.IntegerField(default=0)
    winner = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class gamelog(models.Model):
    gamelog_id = models.CharField(max_length=50, primary_key=True)
    text = models.CharField(max_length=50)
    display = models.CharField(max_length=5000, default="")
    rough = models.CharField(max_length=5000, default="")


class leaderboard(models.Model):
    score_id = models.CharField(max_length=50, primary_key=True)
    word_length = models.IntegerField(default=4)
    difficulty = models.CharField(max_length=20)
    player_id = models.IntegerField(default=0)
    user_name = models.CharField(max_length=100, default='<Imagine your name here, now go play>')
    num_of_turns = models.CharField(max_length=100, default='--')

    def __str__(self):
        return self.name
