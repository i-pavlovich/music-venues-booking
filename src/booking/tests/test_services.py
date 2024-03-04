from datetime import datetime, timedelta

import pytest
from django.utils import timezone

from ..models import Booking, MusicVenue
from ..services import cancel_all_bookings, is_date_available


@pytest.fixture
def current_date() -> datetime:
    return timezone.make_aware(datetime.now(), timezone=timezone.get_current_timezone())


@pytest.fixture
def music_venue() -> MusicVenue:
    return MusicVenue.objects.create(
        name="Long Beach Arena",
        description="The Long Beach Convention and Entertainment Center is a convention center located in Long Beach, California.",
        address="Long Beach, California",
    )


@pytest.fixture
def booking1(music_venue, current_date) -> Booking:
    return Booking.objects.create(
        music_venue=music_venue,
        check_in=current_date,
        check_out=current_date + timedelta(days=3),
        username="Ivan",
        is_active=True,
    )


@pytest.fixture
def booking2(music_venue, current_date) -> Booking:
    return Booking.objects.create(
        music_venue=music_venue,
        check_in=current_date - timedelta(days=5),
        check_out=current_date - timedelta(days=2),
        username="Ivan",
        is_active=True,
    )


@pytest.mark.django_db
def test_cancel_all_bookings(booking1, booking2):
    bookings = Booking.objects.all()
    for booking in bookings:
        assert booking.is_active == True

    cancel_all_bookings()

    bookings = Booking.objects.all()
    for booking in bookings:
        assert booking.is_active == False


@pytest.mark.django_db
def test_is_date_available(booking1, music_venue, current_date):
    # Checking for non-overlapping dates before booking starts
    new_booking = {
        "music_venue": music_venue,
        "check_in": current_date - timedelta(days=5),
        "check_out": current_date - timedelta(days=3),
        "username": "Ivan",
        "is_active": True,
    }
    assert is_date_available(new_booking) == True

    # Checking the overlapping booking end date
    new_booking["check_out"] = current_date + timedelta(days=2)
    assert is_date_available(new_booking) == False

    # The date of an existing booking overlaps completely with the date of a new booking
    new_booking["check_in"] = current_date + timedelta(days=1)
    assert is_date_available(new_booking) == False

    # Checking the overlapping booking start date
    new_booking["check_out"] = current_date + timedelta(days=5)
    assert is_date_available(new_booking) == False

    # Checking for non-overlapping dates after the booking has been finished
    new_booking["check_in"] = current_date + timedelta(days=4)
    assert is_date_available(new_booking) == True
