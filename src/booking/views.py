from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from .models import Booking, MusicVenue, Service
from .serializers import BookingSerializer, MusicVenueSerializer, ServiceSerializer
from .services import is_date_available


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
        queryset = Booking.objects.all().select_related("music_venue")
        username = self.request.query_params.get("username")
        if username is not None:
            queryset = queryset.filter(username=username)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = Booking(**serializer.validated_data)

        if is_date_available(booking):
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        raise APIException(
            detail="The selected date is already taken",
            code=status.HTTP_400_BAD_REQUEST,
        )
