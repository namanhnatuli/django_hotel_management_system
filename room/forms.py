from django import forms
from django.forms import ModelForm, NumberInput

from room.models import Facility, RoomType, Room


class FacilityForm(ModelForm):
    class Meta:
        model = Facility
        fields = '__all__'
        widgets = {
            'facility_type': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
        }


class RoomTypeForm(ModelForm):
    facility = forms.ModelMultipleChoiceField(queryset=Facility.objects.all(), required=False, widget=forms.CheckboxSelectMultiple, label='Co so vat chat')
    description = forms.CharField(label='Mo ta', max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control form-control-user'}))

    class Meta:
        model = RoomType
        fields = '__all__'
        widgets = {
            'type': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'price': forms.NumberInput(attrs={'class': 'form-control form-control-user'}),
        }


class RoomForm(ModelForm):

    class Meta:
        model = Room
        fields = '__all__'
        widgets = {
            'room_number': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'room_type': forms.Select(attrs={'class': 'form-control form-control-user'}),
            'availability': forms.HiddenInput,
        }


