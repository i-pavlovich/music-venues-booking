from django.urls import path

from .views import (
    BookingDetail,
    BookingList,
    CancelAllBookings,
    MusicVenueDetail,
    MusicVenueList,
    ServiceDetail,
    ServiceList,
)


urlpatterns = [
    path("booking_list/", BookingList.as_view(), name="booking_list"),
    path("booking/<int:pk>", BookingDetail.as_view(), name="booking_detail"),
    path("music_venue_list/", MusicVenueList.as_view(), name="music_venue_list"),
    path(
        "music_venue/<int:pk>/", MusicVenueDetail.as_view(), name="music_venue_detail"
    ),
    path("service_list/", ServiceList.as_view(), name="service_list"),
    path("service/<int:pk>", ServiceDetail.as_view(), name="service_detail"),
    path(
        "cancel_all_bookings/", CancelAllBookings.as_view(), name="cancel_all_bookings"
    ),
]
