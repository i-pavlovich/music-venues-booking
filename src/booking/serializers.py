from rest_framework import serializers

from .models import Booking, MusicVenue, Service


class MusicVenueSerializer(serializers.ModelSerializer):
    services = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )

    class Meta:
        model = MusicVenue
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    music_venue = serializers.SlugRelatedField(
        queryset=MusicVenue.objects.all(),
        slug_field="name",
    )

    class Meta:
        model = Booking
        fields = "__all__"
