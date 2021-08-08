from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


class StaffRole(models.Model):
    role = models.CharField('Bo phan', max_length=50)

    def __str__(self):
        return self.role


class Staff(models.Model):
    GENDER = (
        ('M', 'Nam'),
        ('F', 'Nu'),
    )
    staff_id = models.CharField('Ma nhan vien', primary_key=True, max_length=10,
                                error_messages={'unique': "Ma nhan vien da ton tai"})
    first_name = models.CharField('Ho va ten dem', max_length=50)
    last_name = models.CharField('Ten', max_length=50)
    staff_role = models.ForeignKey(StaffRole, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Bo phan')
    staff_email = models.EmailField('Email', unique=True, error_messages={'unique': "Email da duoc su dung"})
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, editable=False)

    class Meta:
        ordering = ['first_name', 'last_name', 'staff_id']

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    def get_absolute_url(self):
        return reverse('staff_detail', args=[str(self.staff_id)])

