from django.db.models import Q

from .models import Booking


def is_date_available(booking: Booking) -> bool:
    overlapping_bookings = Booking.objects.filter(
        Q(music_venue=booking.music_venue)
        & (
            Q(check_in__range=(booking.check_in, booking.check_out))
            | Q(check_out__range=(booking.check_in, booking.check_out))
        )
    )
    return not overlapping_bookings.exists()


def cancel_all_bookings() -> None:
    Booking.objects.all().update(is_active=False)
