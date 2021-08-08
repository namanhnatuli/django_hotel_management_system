import datetime

from django import forms
from django.contrib.admin import widgets
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils import timezone

from booking.models import Booking, CheckIn, Service, CheckOut
from room.models import Room
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'service_type': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'service_price': forms.NumberInput(attrs={'class': 'form-control form-control-user'}),
        }


class BookingForm(ModelForm):
    arrival_date_time = forms.SplitDateTimeField(label='Ngay den', widget=widgets.AdminSplitDateTime())
    departure_date_time = forms.SplitDateTimeField(label='Ngay du kien di', widget=widgets.AdminSplitDateTime())

    def clean(self):
        super(BookingForm, self).clean()
        arrival_date_time = self.cleaned_data['arrival_date_time']
        departure_date_time = self.cleaned_data['departure_date_time']
        if arrival_date_time < timezone.now():
            raise ValidationError(_('Ngay du kien den khong hop le'))
        if departure_date_time < arrival_date_time:
            raise ValidationError(_('Ngay du kien di khong hop le'))

    class Meta:
        model = Booking
        fields = '__all__'
        exclude = ['user', 'booking_date_time', 'updated_at', 'canceled']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control form-control-user', 'rows': "3"}),
        }


class BookingUpdateForm(ModelForm):
    arrival_date_time = forms.SplitDateTimeField(label='Ngay den', widget=widgets.AdminSplitDateTime())
    departure_date_time = forms.SplitDateTimeField(label='Ngay du kien di', widget=widgets.AdminSplitDateTime())

    def clean(self):
        super(BookingUpdateForm, self).clean()
        arrival_date_time = self.cleaned_data['arrival_date_time']
        departure_date_time = self.cleaned_data['departure_date_time']
        if arrival_date_time < timezone.now():
            raise ValidationError(_('Ngay du kien den khong hop le'))
        if departure_date_time < arrival_date_time:
            raise ValidationError(_('Ngay du kien di khong hop le'))

    class Meta:
        model = Booking
        fields = '__all__'
        exclude = ['user', 'booking_date_time', 'updated_at', 'customer', 'booking_type', 'canceled']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control form-control-user', 'rows': "3"}),
        }


class BookingCancelRequestForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['canceled']
        widgets = {'canceled': forms.HiddenInput, }


class CheckInForm(ModelForm):
    class Meta:
        model = CheckIn
        fields = ['services', 'rooms', 'departure_date_time']

    def __init__(self, *args, **kwargs):
        super(CheckInForm, self).__init__(*args, **kwargs)
        rooms_number = [room.room_number for room in self.instance.rooms.all()]
        self.fields['rooms'].queryset = Room.objects.filter(
            Q(room_number__in=rooms_number) | (Q(availability=True) & Q(maintenance=False)))

    rooms = forms.ModelMultipleChoiceField(
        queryset=Room.objects.filter(Q(availability=True) & Q(maintenance=False)),
        required=True, widget=forms.CheckboxSelectMultiple, label='Phong thue', )

    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(), required=False,
        widget=forms.CheckboxSelectMultiple, label='Dich vu')

    departure_date_time = forms.SplitDateTimeField(label='Ngay tra phong', widget=widgets.AdminSplitDateTime())

    def clean(self):
        super(CheckInForm, self).clean()
        departure_date_time = self.cleaned_data['departure_date_time']
        if departure_date_time < timezone.now():
            raise ValidationError(_('Ngay tra phong khong hop le'))


class CheckOutForm(ModelForm):
    class Meta:
        model = CheckOut
        fields = ['extra_fee', 'discount', 'vat', 'payment_type']
        widgets = {
            'payment_type': forms.Select(attrs={'class': 'form-control form-control-user'}),
            'extra_fee': forms.NumberInput(attrs={'class': 'form-control form-control-user'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control form-control-user'}),
            'vat': forms.NumberInput(attrs={'class': 'form-control form-control-user'}),
        }
