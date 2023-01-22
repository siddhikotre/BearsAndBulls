from django.db import models
# Create your models here.
class word(models.Model):
    word_id = models.IntegerField()
    word = models.CharField(max_length=50)
    length = models.IntegerField(default=4)
    difficulty = models.CharField(max_length=20, default= "easy")
    description = models.CharField(max_length=200, default= "Description not available")

    def __str__(self):
        return self.name

class game(models.Model):
    player_id = models.IntegerField()
    game_id = models.IntegerField()
    game_date = models.DateField(auto_now_add=True)
    opponent_id = models.IntegerField(default=0)
    is_active = models.IntegerField(default=0)
    player_mode = models.CharField(max_length=20)
    word_length = models.IntegerField()
    difficulty = models.CharField(max_length=20)
    word = models.CharField(max_length=20)
    p1_score = models.IntegerField(default=0)
    p2_score = models.IntegerField(default=0)
    winner = models.IntegerField()

    def __str__(self):
        return self.name
