from django import forms
from django.forms import ModelForm

from customer.models import Customer


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'customer_dob': forms.DateInput(attrs={'class': 'form-control form-control-user'}),
            'customer_adress': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control form-control-user'}),
        }
