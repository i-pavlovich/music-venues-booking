from datetime import datetime, timedelta

import pytest
from django.db import IntegrityError

from ..models import Booking, MusicVenue, Service


@pytest.fixture
def service1() -> Service:
    return Service.objects.create(name="Audio equipment")


@pytest.fixture
def service2() -> Service:
    return Service.objects.create(name="Covered area")


@pytest.fixture
def music_venue() -> MusicVenue:
    return MusicVenue.objects.create(
        name="Long Beach Arena",
        description="The Long Beach Convention and Entertainment Center is a convention center located in Long Beach, California.",
        address="Long Beach, California",
    )


@pytest.fixture
def booking(music_venue) -> Booking:
    return Booking.objects.create(
        music_venue=music_venue,
        check_in=datetime.utcnow(),
        check_out=datetime.utcnow() + timedelta(days=3),
        username="Ivan",
        is_active=True,
    )


@pytest.mark.django_db
def test_service_name_max_length(service1):
    max_length = service1._meta.get_field("name").max_length
    assert max_length == 150


@pytest.mark.django_db
def test_service_str(service1):
    assert str(service1) == "Audio equipment"


@pytest.mark.django_db
def test_music_venue_name_max_length(music_venue):
    max_length = music_venue._meta.get_field("name").max_length
    assert max_length == 150


@pytest.mark.django_db
def test_music_venue_description_max_length(music_venue):
    max_length = music_venue._meta.get_field("description").max_length
    assert max_length == 2000


@pytest.mark.django_db
def test_music_venue_address_max_length(music_venue):
    max_length = music_venue._meta.get_field("address").max_length
    assert max_length == 150


@pytest.mark.django_db
def test_music_venue_services_verbose_name(music_venue):
    verbose_name = music_venue._meta.get_field("services").verbose_name
    assert verbose_name == "available services"


@pytest.mark.django_db
def test_music_venue_str(music_venue):
    assert str(music_venue) == "Long Beach Arena"


@pytest.mark.django_db
def test_music_venue_services(music_venue, service1, service2):
    music_venue.services.add(service1, service2)
    assert music_venue.services.count() == 2
    assert music_venue.services.first().name == "Audio equipment"
    assert music_venue.services.last().name == "Covered area"


@pytest.mark.django_db
def test_music_venue_services_backref(music_venue, service1, service2):
    music_venue2 = MusicVenue.objects.create(
        name="El Rey Theatre",
        description="The El Rey Theatre is a live music venue in the Miracle Mile area of the Mid-Wilshire region in Los Angeles, California.",
        address="Los Angeles, California",
    )
    music_venue.services.add(service1, service2)
    music_venue2.services.add(service1)
    assert len(service1.musicvenue_set.all()) == 2
    assert len(service2.musicvenue_set.all()) == 1


@pytest.mark.django_db
def test_booking_username_max_length(booking):
    max_length = booking._meta.get_field("username").max_length
    assert max_length == 100


@pytest.mark.django_db
def test_booking_is_active_default_value(booking):
    default_value = booking._meta.get_field("is_active").default
    assert default_value == True


@pytest.mark.django_db
def test_booking_music_venue_on_delete(booking, music_venue):
    with pytest.raises(IntegrityError):
        music_venue.delete()
    booking.delete()
    music_venue.delete()


@pytest.mark.django_db
def test_booking_str(booking):
    assert str(booking) == "Long Beach Arena music venue is booked by user Ivan"
