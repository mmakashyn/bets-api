from rest_framework import serializers
from .models import BetHistory


class BetHistorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = BetHistory
        fields = (
            "id",
            "device_id",
            "bet",
            "win_on_bet",
            "total_bet",
            "potential_win"
        )


class ParticipantSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=256)
    name = serializers.CharField(max_length=256)
    logo = serializers.CharField(max_length=256)
    score = serializers.IntegerField()
    attacks = serializers.IntegerField()
    shoots = serializers.IntegerField()
    winCoef = serializers.FloatField()


class EntrySerializer(serializers.Serializer):
    id = serializers.CharField(max_length=256)
    tournamentLogo = serializers.CharField(max_length=256)
    tournamentTitle = serializers.CharField(max_length=256)
    time = serializers.DateTimeField()
    drawCoef = serializers.FloatField()
    duration = serializers.CharField(max_length=256)
    participant = ParticipantSerializer(many=True)
