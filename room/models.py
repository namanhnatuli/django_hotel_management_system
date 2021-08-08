from django.db import models

# Create your models here.
from django.urls import reverse


class Facility(models.Model):
    facility_type = models.CharField('Co so vat chat', max_length=50, unique=True, error_messages={'unique':"truong thong tin da ton tai"})

    def __str__(self):
        return self.facility_type


class RoomType(models.Model):
    type = models.CharField('Loai phong', max_length=50, unique=True, error_messages={'unique':"Loai phong da ton tai"})
    facility = models.ManyToManyField(Facility, verbose_name='Co so vat chat')
    description = models.CharField('Mo ta', max_length=1000, null=True, blank=True)
    price = models.FloatField('Gia phong')

    class Meta:
        ordering = ['price']

    def __str__(self):
        return self.type


class Room(models.Model):
    room_number = models.CharField('So phong', primary_key=True, max_length=30, error_messages={'unique':"Phong da ton tai"})
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True, verbose_name="Loai phong")
    maintenance = models.BooleanField(default=False, verbose_name='Bao tri')
    availability = models.BooleanField(default=True, verbose_name='Co the su dung')

    class Meta:
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f'{self.room_number} - {self.room_type}'

    def get_absolute_url(self):
        return reverse('room_detail', args=[str(self.room_number)])

