import requests
import random

from django.conf import settings
from datetime import datetime, timedelta

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import ListAPIView

from rest_framework import mixins, status
from .serializers import BetHistorySerializer
from .models import BetHistory
from .tests import RANDOM_IMAGES


# Create your views here.
class BetHistoryViewSet(GenericViewSet, mixins.CreateModelMixin):
    serializer_class = BetHistorySerializer
    queryset = BetHistory.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class AbstractMatchesView(APIView):
    """
    Abstract class for getting and routing data from RAPID API
    required parameters: api_url, rapid_api_host
    """
    api_url = ""
    rapid_api_host = ""

    @property
    def querystring(self):
        querystring = {"Category": "soccer", "Timezone": "-7"}
        return querystring

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")

        if pk:
            data = self.get_details_data(pk)
        else:
            data = self.get_list_data()

        return Response(data, status=status.HTTP_200_OK)

    def get_list_data(self):
        url = self.api_url
        headers = {
            "X-RapidAPI-Key": settings.RAPID_API_KEY,
            "X-RapidAPI-Host": self.rapid_api_host
        }

        response = requests.get(url, headers=headers, params=self.querystring)
        # data = [self.get_clean_response_data(item) for item in response.json()]
        data = [self.get_clean_response_data(item) for item in range(random.randint(10, 80))]  # TODO: Remove test data
        return data

    def get_details_data(self, pk):
        # url = self.api_url + f"/{pk}"
        url = self.api_url + "/41881"
        headers = {
            "X-RapidAPI-Key": settings.RAPID_API_KEY,
            "X-RapidAPI-Host": self.rapid_api_host
        }
        response = requests.get(url, headers=headers, params=self.querystring)
        data = self.get_clean_response_data(response)
        return data

    def get_clean_response_data(self, item):  # TODO: implement transformation data response
        """
        Generate random data for testing
        """
        # entry = {
        #     'id': random.randint(1, 100),
        #     'tournamentLogo': random.choice(RANDOM_IMAGES),
        #     'tournamentTitle': f"Tournament {random.randint(1, 10)}",
        #     'participant1': f"Team {random.choice(['A', 'B', 'C', 'D'])}",
        #     'participant2': f"Team {random.choice(['E', 'F', 'G', 'H'])}",
        #     'time': datetime.now() + timedelta(days=random.randint(1, 30)),
        #     'participant1Coef': round(random.uniform(1, 5), 2),
        #     'participant2Coef': round(random.uniform(1, 5), 2),
        #     'draw': round(random.uniform(1, 5), 2),
        # }
        entry = {
            'id': random.randint(1, 100),
            'tournamentLogo': random.choice(RANDOM_IMAGES),
            'tournamentTitle': f"Tournament {random.randint(1, 10)}",
            'time': datetime.now() + timedelta(days=random.randint(1, 30)),
            'drawCoef': round(random.uniform(1, 5), 2),
            'duration': f"{random.randint(0, 2)}:{random.randint(0, 59)}:{random.randint(0, 59)}",
            'participant': [
                {
                    "id": random.randint(1, 100),
                    "name": f"Team {random.choice(['A', 'B', 'C', 'D'])}",
                    "logo": random.choice(RANDOM_IMAGES),
                    "score": random.randint(1, 5),
                    "attacks": random.randint(1, 50),
                    "shoots": random.randint(1, 50),
                    "winCoef": round(random.uniform(1, 5), 2),
                },
                {
                    "id": random.randint(1, 100),
                    "name": f"Team {random.choice(['A', 'B', 'C', 'D'])}",
                    "logo": random.choice(RANDOM_IMAGES),
                    "score": random.randint(1, 5),
                    "attacks": random.randint(1, 50),
                    "shoots": random.randint(1, 50),
                    "winCoef": round(random.uniform(1, 5), 2),
                },
            ],
        }

        return entry


class CricketMatchesView(AbstractMatchesView):
    api_url = "https://livescore6.p.rapidapi.com/matches/v2/list-live"
    rapid_api_host = "livescore6.p.rapidapi.com"


class FootballMatchesView(CricketMatchesView):
    pass


class BasketballMatchesView(CricketMatchesView):
    pass


class GolfMatchesView(CricketMatchesView):
    pass


class RugbyMatchesView(CricketMatchesView):
    pass
