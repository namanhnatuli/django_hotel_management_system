from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils import timezone


class Customer(models.Model):
    customer_name = models.CharField("Ten khach hang", max_length=100)
    customer_dob = models.DateTimeField("Ngay sinh", default=timezone.now)
    customer_adress = models.CharField('Dia chi', max_length=400, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?\d{8,11}$', message="Nhap so dien thoai theo dinh dang: 0123456789")
    customer_phone = models.CharField('So dien thoai', validators=[phone_regex], max_length=13, blank=True)
    customer_email = models.EmailField("Email")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngay tao')

    class Meta:
        ordering = ['customer_name']

    def __str__(self):
        return f'{self.customer_name}, SDT: {self.customer_phone}, Email: {self.customer_email}'

    def get_absolute_url(self):
        return reverse('customer_detail', args=[str(self.id)])
