from rest_framework import serializers

from .models import Booking, MusicVenue, Service
from .services import is_date_available
from .validators import is_correct_time_period


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

    def validate(self, attrs):
        if not is_correct_time_period(attrs):
            raise serializers.ValidationError(
                {"Invalid date": "Set the correct time period"}
            )
        if not is_date_available(attrs):
            raise serializers.ValidationError(
                {"Invalid date": "The selected date is already taken"}
            )
        return attrs
