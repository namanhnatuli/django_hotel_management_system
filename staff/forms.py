from django.forms import ModelForm
from django import forms
from staff.models import Staff, StaffRole


class StaffRoleForm(ModelForm):
    class Meta:
        model = StaffRole
        fields = '__all__'
        widgets = {
            'role': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
        }


class StaffForm(ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'
        widgets = {
            'staff_id': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'staff_role': forms.Select(attrs={'class': 'form-control form-control-user'}),
            'staff_email': forms.EmailInput(attrs={'class': 'form-control form-control-user'}),
        }
