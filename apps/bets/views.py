import requests
import random

from django.conf import settings
from datetime import (
    datetime,
    timedelta,
)

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import ListAPIView

from .models import BetHistory
from .tests import RANDOM_IMAGES
from rest_framework import (
    mixins,
    status,
)
from .serializers import (
    BetHistorySerializer,
    EntrySerializer
)


class BetHistoryViewSet(GenericViewSet, mixins.CreateModelMixin):
    serializer_class = BetHistorySerializer
    queryset = BetHistory.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class AbstractMatchesView(ListAPIView):
    """
    Abstract class for getting and routing data from RAPID API
    required parameters: api_url, rapid_api_host
    """
    api_url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-date"
    rapid_api_host = "livescore6.p.rapidapi.com"
    game_name = ""
    serializer_class = EntrySerializer
    page_size = 10

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        data = self.get_queryset(pk)
        serializer = self.get_serializer(data=data, many=isinstance(data, list))

        # Check if the serializer is valid
        serializer.is_valid()

        if not pk:
            page = self.paginate_queryset(data)

            serializer_context = {'request': request}
            serializer = self.serializer_class(
                page, context=serializer_context, many=True
            )
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @property
    def querystring(self):
        date = datetime.now()
        querystring = {
            "Category": self.game_name,
            "Date": f"{date.year}{date.month}{date}",
            "Timezone": "-7"
        }
        return querystring

    def get_queryset(self, pk=None):
        headers = {
            "X-RapidAPI-Key": settings.RAPID_API_KEY,
            "X-RapidAPI-Host": self.rapid_api_host
        }

        try:
            # Make the API request
            response = requests.get(self.api_url, headers=headers, params=self.querystring)
            response.raise_for_status()

            # Extract relevant data from the response
            data = response.json()
            data = data["Stages"]

            competition_data = []
            for tournament in data:
                for game in tournament["Events"]:

                    entry = {
                        'id': game["Eid"],
                        'tournamentLogo': tournament.get('badgeUrl'),
                        'tournamentTitle': tournament['Scd'],
                        'time': datetime.now() + timedelta(days=random.randint(1, 30)),
                        'drawCoef': round(random.uniform(1, 5), 2),
                        'duration': f"{random.randint(0, 2)}:{random.randint(0, 59)}:{random.randint(0, 59)}",
                        'participant': [
                            {
                                "id": game["T1"][0].get('ID'),
                                "name": game["T1"][0].get('Nm'),
                                "logo": game["T1"][0].get('Img'),
                                "score": random.randint(1, 5),
                                "attacks": random.randint(1, 50),
                                "shoots": random.randint(1, 50),
                                "winCoef": round(random.uniform(1, 5), 2),
                            },
                            {
                                "id": game["T2"][0].get('ID'),
                                "name": game["T2"][0].get('Nm'),
                                "logo": game["T2"][0].get('Img'),
                                "score": random.randint(1, 5),
                                "attacks": random.randint(1, 50),
                                "shoots": random.randint(1, 50),
                                "winCoef": round(random.uniform(1, 5), 2),
                            },
                        ],
                    }
                    if pk == int(entry.get('id')):
                        return entry

                    competition_data.append(entry)

            return competition_data

        except requests.RequestException as e:
            # Handle any request-related exceptions
            print(f"Error making API request: {e}")
            return Response({"error": "Error making API request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            # Handle other unexpected exceptions
            print(f"Unexpected error: {e}")
            return Response({"error": "Unexpected error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SoccerMatchesView(AbstractMatchesView):
    game_name = 'soccer'


class CricketMatchesView(AbstractMatchesView):
    game_name = 'cricket'


class BasketballMatchesView(AbstractMatchesView):
    game_name = 'basketball'


class HockeyMatchesView(AbstractMatchesView):
    game_name = 'hockey'


# =============================TEST DATA============================

class TestDataMatchesView(APIView):
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
            data = self.get_list_data(pk)

        return Response(data, status=status.HTTP_200_OK)

    def get_list_data(self, pk=None):
        url = self.api_url
        headers = {
            "X-RapidAPI-Key": settings.RAPID_API_KEY,
            "X-RapidAPI-Host": self.rapid_api_host
        }

        try:
            # Make the API request
            response = requests.get(url, headers=headers, params=self.querystring)
            response.raise_for_status()

            # Extract relevant data from the response
            data = response.json()

            # Return the extracted data in the DRF Response object
            data = [self.get_clean_response_data(item) for item in range(random.randint(10, 80))]
            return data

        except requests.RequestException as e:
            # Handle any request-related exceptions
            print(f"Error making API request: {e}")
            return Response({"error": "Error making API request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            # Handle other unexpected exceptions
            print(f"Unexpected error: {e}")
            return Response({"error": "Unexpected error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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


class GolfMatchesView(TestDataMatchesView):
    api_url = "https://livescore6.p.rapidapi.com/matches/v2/list-live"
    rapid_api_host = "livescore6.p.rapidapi.com"


class RugbyMatchesView(TestDataMatchesView):
    api_url = "https://livescore6.p.rapidapi.com/matches/v2/list-live"
    rapid_api_host = "livescore6.p.rapidapi.com"


#
#
# class SoccerMatchesView(AbstractMatchesView):
#     api_url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-date"
#     rapid_api_host = "livescore6.p.rapidapi.com"
#     game_name = 'soccer'
#
#     @property
#     def querystring(self):
#         date = datetime.now()
#         querystring = {
#             "Category": self.game_name,
#             "Date": f"{date.year}{date.month}{date}",
#             "Timezone": "-7"
#         }
#         return querystring
#
#     def get_list_data(self, pk=None):
#         headers = {
#             "X-RapidAPI-Key": settings.RAPID_API_KEY,
#             "X-RapidAPI-Host": self.rapid_api_host
#         }
#
#         try:
#             # Make the API request
#             response = requests.get(self.api_url, headers=headers, params=self.querystring)
#             response.raise_for_status()
#
#             # Extract relevant data from the response
#             data = response.json()
#             data = data["Stages"]
#
#             competition_data = []
#             for tournament in data:
#                 for game in tournament["Events"]:
#
#                     entry = {
#                         'id': game["Eid"],
#                         'tournamentLogo': tournament.get('badgeUrl'),
#                         'tournamentTitle': tournament['Scd'],
#                         'time': datetime.now() + timedelta(days=random.randint(1, 30)),
#                         'drawCoef': round(random.uniform(1, 5), 2),
#                         'duration': f"{random.randint(0, 2)}:{random.randint(0, 59)}:{random.randint(0, 59)}",
#                         'participant': [
#                             {
#                                 "id": game["T1"][0].get('ID'),
#                                 "name": game["T1"][0].get('Nm'),
#                                 "logo": game["T1"][0].get('Img'),
#                                 "score": random.randint(1, 5),
#                                 "attacks": random.randint(1, 50),
#                                 "shoots": random.randint(1, 50),
#                                 "winCoef": round(random.uniform(1, 5), 2),
#                             },
#                             {
#                                 "id": game["T2"][0].get('ID'),
#                                 "name": game["T2"][0].get('Nm'),
#                                 "logo": game["T2"][0].get('Img'),
#                                 "score": random.randint(1, 5),
#                                 "attacks": random.randint(1, 50),
#                                 "shoots": random.randint(1, 50),
#                                 "winCoef": round(random.uniform(1, 5), 2),
#                             },
#                         ],
#                     }
#                     if pk == int(entry.get('id')):
#                         return entry
#
#                     competition_data.append(entry)
#
#             return self.get_paginated_response(competition_data)
#
#         except requests.RequestException as e:
#             # Handle any request-related exceptions
#             print(f"Error making API request: {e}")
#             return Response({"error": "Error making API request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#         except Exception as e:
#             # Handle other unexpected exceptions
#             print(f"Unexpected error: {e}")
#             return Response({"error": "Unexpected error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     def get_details_data(self, pk):
#         url = self.api_url + f"/{pk}"
#         headers = {
#             "X-RapidAPI-Key": settings.RAPID_API_KEY,
#             "X-RapidAPI-Host": self.rapid_api_host
#         }
#         response = requests.get(url, headers=headers, params=self.querystring)
#         data = self.get_clean_response_data(response)
#         return data
