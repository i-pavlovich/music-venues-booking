from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, MusicVenue, Service
from .serializers import BookingSerializer, MusicVenueSerializer, ServiceSerializer
from .services import cancel_all_bookings


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


class CancelAllBookings(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        cancel_all_bookings()
        return Response({"Success": "All bookings have been cancelled"})
