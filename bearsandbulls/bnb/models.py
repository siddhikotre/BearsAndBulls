from django.db import models


# Create your models here.
class word(models.Model):
    word_id = models.IntegerField(primary_key=True)
    word = models.CharField(max_length=50)
    length = models.IntegerField(default=4)
    difficulty = models.CharField(max_length=20, default="easy")
    description = models.CharField(max_length=200, default="Description not available")

    def __str__(self):
        return self.name


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
    gamelog_id = models.CharField(max_length=50,primary_key=True)
    text = models.CharField(max_length=50)
    display = models.CharField(max_length=5000)

    def __str__(self):
        return self.name
