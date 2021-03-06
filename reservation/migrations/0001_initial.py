# Generated by Django 3.2.6 on 2021-08-08 08:35

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest_name', models.CharField(max_length=300, verbose_name='Ho va ten')),
                ('guest_phone', models.CharField(blank=True, max_length=13, validators=[django.core.validators.RegexValidator(message='Nhap so dien thoai theo dinh dang: 0123456789', regex='^\\+?\\d{8,11}$')], verbose_name='So dien thoai')),
                ('guest_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('no_of_children', models.PositiveSmallIntegerField(default=0, verbose_name='So tre nho')),
                ('no_of_adults', models.PositiveSmallIntegerField(default=1, verbose_name='So nguoi lon')),
                ('reservation_date_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Ngay dat')),
                ('expected_arrival_date_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Ngay den du kien')),
                ('expected_departure_date_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Ngay di du kien')),
                ('description', models.CharField(blank=True, max_length=3000, null=True, verbose_name='Yeu cau cua khach hang')),
                ('status', models.CharField(choices=[('Cho xu ly', 'Cho xu ly'), ('Da dat phong', 'Da dat phong'), ('Da huy', 'Da huy')], default='Cho xu ly', max_length=20, verbose_name='Trang thai')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Cap nhat luc')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Nguoi xu ly')),
            ],
            options={
                'ordering': ['reservation_date_time', 'expected_arrival_date_time', 'guest_name'],
            },
        ),
    ]
