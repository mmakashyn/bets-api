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
