from django.db import models

# Create your models here.


class BetHistory(models.Model):
    device_id = models.CharField(max_length=100)
    bet = models.IntegerField()
    win_on_bet = models.IntegerField()
    total_bet = models.IntegerField()
    potential_win = models.IntegerField()

    def __str__(self):
        return f"Bet {self.device_id}"

    class Meta:
        verbose_name_plural = "Bet History"
        verbose_name = "Bet History"
        app_label = "bets"
