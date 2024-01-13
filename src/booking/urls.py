from django.urls import path

from .views import (
    BookingDetail,
    BookingList,
    MusicVenueDetail,
    MusicVenueList,
    ServiceDetail,
    ServiceList,
)


urlpatterns = [
    path("booking/", BookingList.as_view()),
    path("booking/<int:pk>", BookingDetail.as_view()),
    path("music_venues/", MusicVenueList.as_view()),
    path("music_venue/<int:pk>/", MusicVenueDetail.as_view()),
    path("services/", ServiceList.as_view()),
    path("service/<int:pk>", ServiceDetail.as_view()),
]
