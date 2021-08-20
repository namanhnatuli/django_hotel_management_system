from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils import timezone


class Reservation(models.Model):
    STATUS = (
        ('Cho xu ly', 'Cho xu ly'),
        ('Da dat phong', 'Da dat phong'),
        ('Da huy', 'Da huy'),
    )
    guest_name = models.CharField('Ho va ten', max_length=300)
    phone_regex = RegexValidator(regex=r'^\+?\d{8,11}$', message="Nhap so dien thoai theo dinh dang: 0123456789")
    guest_phone = models.CharField('So dien thoai', validators=[phone_regex], max_length=13, blank=True)
    guest_email = models.EmailField("Email", null=True, blank=True)
    no_of_children = models.PositiveSmallIntegerField("So tre nho", default=0)
    no_of_adults = models.PositiveSmallIntegerField("So nguoi lon", default=1)
    reservation_date_time = models.DateTimeField("Ngay dat", default=timezone.now)
    expected_arrival_date_time = models.DateTimeField("Ngay den du kien", default=timezone.now)
    expected_departure_date_time = models.DateTimeField("Ngay di du kien", default=timezone.now)
    status = models.CharField('Trang thai', max_length=20, choices=STATUS, default='Cho xu ly')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Nguoi xu ly')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Cap nhat luc')

    class Meta:
        ordering = ['reservation_date_time', 'expected_arrival_date_time', 'guest_name']

    def get_absolute_url(self):
        return reverse('reservation_detail', args=[str(self.id)])

    def __str__(self):
        return str(self.id)

    def total_guest(self):
        return self.no_of_adults + self.no_of_children

    @property
    def is_over_expected_arrival_time(self):
        if self.expected_arrival_date_time and timezone.now() > self.expected_arrival_date_time:
            return True
        return False
