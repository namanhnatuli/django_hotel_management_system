from math import ceil

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

from customer.models import Customer
from reservation.models import Reservation
from room.models import Room
from staff.models import Staff


class Service(models.Model):
    service_type = models.CharField('Dich vu', max_length=50)
    service_price = models.FloatField('Gia', default=0)

    class Meta:
        ordering = ['service_price', 'service_type']

    def __str__(self):
        return self.service_type


class BookingType(models.Model):
    booking_type = models.CharField('Hinh thuc dat phong', max_length=50)

    def __str__(self):
        return self.booking_type


class Booking(models.Model):
    booking_type = models.ForeignKey(BookingType, on_delete=models.SET_NULL, null=True, default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Nguoi thuc hien')
    no_of_adults = models.PositiveSmallIntegerField(default=1, verbose_name='So nguoi lon')
    no_of_children = models.PositiveSmallIntegerField(default=0, verbose_name='So tre em')
    booking_date_time = models.DateTimeField(default=timezone.now, verbose_name='Ngay dat phong')
    arrival_date_time = models.DateTimeField(default=timezone.now, verbose_name='Ngay den')
    departure_date_time = models.DateTimeField(default=timezone.now, verbose_name='Ngay du kien di')
    description = models.CharField("Yeu cau cua khach hang", max_length=3000, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='cap nhat luc')
    canceled = models.BooleanField(default=False, verbose_name='Huy dat truoc', blank=True, null=True)

    class Meta:
        ordering = ['arrival_date_time', 'booking_date_time']

    def get_absolute_url(self):
        return reverse('booking_detail', args=[str(self.id)])

    def __str__(self):
        return f'({self.id}) {self.customer}'

    def total_guest(self):
        return self.no_of_adults + self.no_of_children

    @property
    def is_over_arrival_time(self):
        if self.arrival_date_time and timezone.now() > self.arrival_date_time:
            return True
        return False


class CheckIn(models.Model):
    id = models.CharField(max_length=50, primary_key=True, blank=True, editable=False)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, null=True)
    rooms = models.ManyToManyField(Room, verbose_name='Phong thue')
    services = models.ManyToManyField(Service, verbose_name='Dich vu')
    departure_date_time = models.DateTimeField(default=timezone.now, verbose_name='Ngay du tra phong')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Nguoi checkin')
    checkin_time = models.DateTimeField(auto_now_add=True, verbose_name='Thoi gian check in')
    initial_amount = models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='Tien/ngay')

    updated_at = models.DateTimeField(auto_now=True, verbose_name='cap nhat luc')

    class Meta:
        ordering = ['-checkin_time']

    def get_absolute_url(self):
        return reverse('checkin_detail', args=[str(self.id)])

    def __str__(self):
        return f'({self.id}) {self.booking.customer.customer_name}'

    def save(self, *args, **kwargs):
        initial_amount = 0
        for room in self.rooms.all():
            initial_amount += room.room_type.price
            for service in self.services.all():
                initial_amount += service.service_price
        self.initial_amount = initial_amount
        super().save(*args, **kwargs)

    @property
    def is_over_departure_time(self):
        if self.departure_date_time and timezone.now() > self.departure_date_time:
            return True
        return False


class CheckOut(models.Model):
    PAYMENT_TYPE = (
        ('Tien mat', 'Tien mat'),
        ('Chuyen khoan', 'Chuyen khoan'),
        ('The thanh toan', 'The thanh toan'),
    )
    id = models.CharField(max_length=50, primary_key=True, blank=True, editable=False)
    checkin = models.OneToOneField(CheckIn, on_delete=models.CASCADE)

    checkout_time = models.DateTimeField(auto_now_add=True, verbose_name='Thoi gian check out')
    stay_duration = models.DurationField(null=True, editable=False, verbose_name='Thoi gian luu tru')
    total_amount = models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='Tong chi phi')
    pay_amount = models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='Thanh tien')

    extra_fee = models.FloatField('Phu phi', default=0)
    discount = models.FloatField('Khuyen mai', default=0)
    vat = models.FloatField("VAT", default=10)
    payment_type = models.CharField('Hinh thuc thanh toan', choices=PAYMENT_TYPE, max_length=20, default='Tien mat')
    checkout_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Nguoi thanh toan")

    class Meta:
        ordering = ['checkout_time']

    def get_absolute_url(self):
        return reverse('checkout_detail', args=[str(self.id)])

    def __str__(self):
        return f'({self.id}) {self.checkin.booking.customer.customer_name}'

    def save(self, *args, **kwargs):
        stay_time = self.checkout_time - self.checkin.checkin_time
        calculated_duration = timezone.timedelta(days=ceil(stay_time.total_seconds() / 3600 / 24))
        self.stay_duration = calculated_duration
        self.total_amount = calculated_duration.days * self.checkin.initial_amount + self.extra_fee
        amount_with_vat = self.total_amount + self.total_amount * self.vat / 100
        self.pay_amount = amount_with_vat - amount_with_vat * self.discount / 100
        super().save(*args, **kwargs)

