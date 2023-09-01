from django.db import models

class GameType(models.Model):
    
    genre = models.CharField(max_length=20)
    label = models.CharField(max_length=100, default="Default Label")