from django.db import models
# Create your models here.
class word(models.Model):
    wordid = models.IntegerField()
    word = models.CharField(max_length=50)

    def __str__(self):
        return self.name
