from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from .serializers import BetHistorySerializer
from .models import BetHistory


# Create your views here.
class BetHistoryViewSet(GenericViewSet, mixins.CreateModelMixin):
    serializer_class = BetHistorySerializer
    queryset = BetHistory.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)