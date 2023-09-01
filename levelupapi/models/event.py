from django.db import models

class Event(models.Model):

    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name="organized_events")
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    attendee = models.ManyToManyField("Gamer", through="GamerEvent", related_name="attended_events")
    event_name = models.CharField(max_length=50)
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="event_games", default=1)