from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=150)


class MusicVenue(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=2000)
    address = models.CharField(max_length=150)
    services = models.ManyToManyField(Service, verbose_name="available services")


class Booking(models.Model):
    music_venue = models.ForeignKey(MusicVenue, on_delete=models.PROTECT)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    username = models.CharField(max_length=100)
