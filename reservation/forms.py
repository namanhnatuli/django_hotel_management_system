from django import forms
from django.contrib.admin import widgets
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from reservation.models import Reservation


class ReservationForm(ModelForm):
    expected_arrival_date_time = forms.DateField(label='Ngay du kien den', widget=widgets.AdminDateWidget(attrs={'type':'date'}))
    expected_departure_date_time = forms.DateField(label='Ngay du kien di', widget=widgets.AdminDateWidget(attrs={'type':'date'}))

    def clean(self):
        super(ReservationForm, self).clean()
        expected_arrival_date_time = self.cleaned_data['expected_arrival_date_time']
        expected_departure_date_time = self.cleaned_data['expected_departure_date_time']
        if expected_arrival_date_time < timezone.now().date():
            raise ValidationError(_('Ngay du kien den khong hop le'))
        if expected_departure_date_time < expected_arrival_date_time:
            raise ValidationError(_('Ngay du kien di khong hop le'))

    class Meta:
        model = Reservation
        fields = '__all__'
        exclude = ['user', 'updated_at', 'status']
        widgets = {
            'reservation_date_time': forms.HiddenInput,
        }


class ReservationUpdateForm(ModelForm):
    expected_arrival_date_time = forms.DateField(label='Ngay du kien den', widget=widgets.AdminDateWidget())
    expected_departure_date_time = forms.DateField(label='Ngay du kien di', widget=widgets.AdminDateWidget())

    def clean(self):
        super(ReservationUpdateForm, self).clean()
        expected_arrival_date_time = self.cleaned_data['expected_arrival_date_time']
        expected_departure_date_time = self.cleaned_data['expected_departure_date_time']
        if expected_departure_date_time < expected_arrival_date_time:
            raise ValidationError(_('Ngay du kien di khong hop le'))

    class Meta:
        model = Reservation
        fields = '__all__'
        exclude = ['user', 'updated_at']
        widgets = {
            'status': forms.Select(),
            'reservation_date_time': forms.HiddenInput,
        }
