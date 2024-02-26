from datetime import datetime

from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from .models import Booking, MusicVenue, Service
from .serializers import BookingSerializer, MusicVenueSerializer, ServiceSerializer
from .services import is_date_available


class BookingDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all().select_related("music_venue")


class BookingList(generics.ListCreateAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        queryset = Booking.objects.all().select_related("music_venue")
        username = self.request.query_params.get("username")
        history = self.request.query_params.get("history")
        if username is not None:
            queryset = queryset.filter(username=username)
        if history is not None:
            if history == "True":
                queryset = queryset.filter(is_active=False)
            elif history == "False":
                queryset = queryset.filter(is_active=True)
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


class MusicVenueDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MusicVenueSerializer
    queryset = MusicVenue.objects.all().prefetch_related("services")


class MusicVenueList(generics.ListCreateAPIView):
    serializer_class = MusicVenueSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name", "address", "services__name"]

    def get_queryset(self):
        queryset = MusicVenue.objects.all().prefetch_related("services")
        name = self.request.query_params.get("name")
        address = self.request.query_params.get("address")
        services = self.request.query_params.get("services")
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        if address is not None:
            queryset = queryset.filter(address__icontains=address)
        if services is not None:
            queryset = queryset.filter(services__name__icontains=services)
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
            queryset = queryset.filter(name__icontains=name)
        return queryset
