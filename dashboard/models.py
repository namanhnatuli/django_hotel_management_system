from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class Profile(models.Model):
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, _("Nam")),
        (GENDER_FEMALE, _("Nu")),
    ]

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
