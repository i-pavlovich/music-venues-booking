from rest_framework import generics

from .models import Booking, MusicVenue, Service
from .serializers import BookingSerializer, MusicVenueSerializer, ServiceSerializer


# TODO: Оптимизация запросов
class MusicVenueDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MusicVenueSerializer
    queryset = MusicVenue.objects.all()


class MusicVenueList(generics.ListCreateAPIView):
    serializer_class = MusicVenueSerializer

    def get_queryset(self):
        queryset = MusicVenue.objects.all().select_related()
        name = self.request.query_params.get("name")
        address = self.request.query_params.get("address")
        if name is not None:
            queryset = queryset.filter(name=name)
        if address is not None:
            queryset = queryset.filter(address=address)
        return queryset


class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()


class ServiceList(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        queryset = Service.objects.all()
        name = self.request.query_params.get("name")
        if name is not None:
            queryset = queryset.filter(name=name)
        return queryset


class BookingDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()


class BookingList(generics.ListCreateAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        queryset = Booking.objects.all()
        username = self.request.query_params.get("username")
        if username is not None:
            queryset = queryset.filter(username=username)
        return queryset
