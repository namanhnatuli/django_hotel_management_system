from django import forms
from django.contrib.admin import widgets
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from reservation.models import Reservation


class ReservationForm(ModelForm):
    expected_arrival_date_time = forms.SplitDateTimeField(label='Ngay du kien den', widget=widgets.AdminSplitDateTime())
    expected_departure_date_time = forms.SplitDateTimeField(label='Ngay du kien di', widget=widgets.AdminSplitDateTime())

    def clean(self):
        super(ReservationForm, self).clean()
        expected_arrival_date_time = self.cleaned_data['expected_arrival_date_time']
        expected_departure_date_time = self.cleaned_data['expected_departure_date_time']
        if expected_arrival_date_time < timezone.now():
            raise ValidationError(_('Ngay du kien den khong hop le'))
        if expected_departure_date_time < expected_arrival_date_time:
            raise ValidationError(_('Ngay du kien di khong hop le'))

    class Meta:
        model = Reservation
        fields = '__all__'
        exclude = ['user', 'updated_at', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control form-control-user', 'rows': "3"}),
            'reservation_date_time': forms.HiddenInput,
        }


class ReservationUpdateForm(ModelForm):
    expected_arrival_date_time = forms.SplitDateTimeField(label='Ngay du kien den', widget=widgets.AdminSplitDateTime())
    expected_departure_date_time = forms.SplitDateTimeField(label='Ngay du kien di', widget=widgets.AdminSplitDateTime())

    def clean(self):
        super(ReservationUpdateForm, self).clean()
        expected_arrival_date_time = self.cleaned_data['expected_arrival_date_time']
        expected_departure_date_time = self.cleaned_data['expected_departure_date_time']
        if expected_arrival_date_time < timezone.now():
            raise ValidationError(_('Ngay du kien den khong hop le'))
        if expected_departure_date_time < expected_arrival_date_time:
            raise ValidationError(_('Ngay du kien di khong hop le'))

    class Meta:
        model = Reservation
        fields = '__all__'
        exclude = ['user', 'updated_at']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control form-control-user', 'rows': "3"}),
            'status': forms.Select(),
            'reservation_date_time': forms.HiddenInput,
        }
