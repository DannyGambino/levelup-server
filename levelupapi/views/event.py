"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game


class EventView(ViewSet):
    """Level up events view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """

        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        
        events = Event.objects.all()

        game_param = request.query_params.get("game")

        if game_param is not None:
            game_id = int(game_param)

            if game_id == 1:
                events = events.filter(game__isnull=False)
            elif game_id == 0:
                events = events.filter(game__isnull=True)

        serialized = EventSerializer(events, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        organizer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["game"])

        event = Event.objects.create(
            event_name=request.data["event_name"],
            date=request.data["date"],
            time=request.data["time"],
            game=game,
            organizer=organizer
        )
        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for a event

        Returns:
            Response -- Empty body with 204 status code
        """

        event = Event.objects.get(pk=pk)
        event.date = request.data["date"]
        event.time = request.data["time"]
        event.event_name = request.data["event_name"]

        gamer = Gamer.objects.get(pk=request.data["organizer"])
        game = Game.objects.get(pk=request.data["game"])
        event.organizer = gamer
        event.game = game
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    
class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    class Meta:
        model = Event
        fields = ('id', 'organizer', 'date', 'time', 'attendee', 'event_name', 'game')