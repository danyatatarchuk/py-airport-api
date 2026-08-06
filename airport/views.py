from rest_framework import viewsets

from airport.models import (
    Airport,
    Airplane,
    AirplaneType,
)
from airport.serializers import (
    AirportSerializer,
    AirplaneSerializer,
    AirplaneTypeSerializer,
)


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
