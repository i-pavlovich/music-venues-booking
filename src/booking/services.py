from .models import Booking


def is_date_available(booking: dict) -> bool:
    overlapping_bookings = Booking.objects.filter(
        music_venue=booking["music_venue"],
        check_in__lt=booking["check_out"],
        check_out__gt=booking["check_in"],
    )
    return not overlapping_bookings.exists()


def cancel_all_bookings() -> None:
    Booking.objects.all().update(is_active=False)
