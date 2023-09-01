from django.db import models

class Game(models.Model):

    name = models.CharField(max_length=30)
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE)
    skill_level = models.CharField(max_length=15, default=1)
    players_needed = models.IntegerField(default=1)