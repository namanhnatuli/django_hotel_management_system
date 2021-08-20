from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
import re

from dashboard.models import Profile
from staff.models import Staff


class NewUserForm(forms.Form):
    error_messages = {
        'password_mismatch': _("Hai mat khau khong trung khop"),
        'id_not_found': _("ID khong hop le"),
        'info_not_matched': _("Thong tin khong trung khop"),
        'username_exists': _("Ten tai khoan da duoc su dung"),
        'staff_username_exists': _("ID da duoc su dung de dang ky tai khoan"),
        'email_exists': _("Email da duoc su dung"),
        'password_length': _("Mat khau chi co do dai 8 - 20 ky tu"),
        'password_digit': _("Mat khau phai chua it nhat 1 ky tu so"),
    }

    staff_id = forms.CharField(label=_('ID'), widget=forms.TextInput(
        attrs={'class': 'form-control form-control-user', 'placeholder': _('Nhap ID'), }))
    first_name = forms.CharField(label=_("Ho"), max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-user', 'placeholder': _('Nhap Ho va ten dem'), }))
    last_name = forms.CharField(label=_("Ten"), max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-user', 'placeholder': _('Nhap ten'), }))
    phone_regex = RegexValidator(regex=r'^\+?\d{8,11}$', message="So dien thoai khong hop le")
    contact_no = forms.CharField(label=_('Contact No'), validators=[phone_regex], max_length=13,
                                 widget=forms.TextInput(attrs={'class': 'form-control form-control-user',
                                                               'placeholder': _('Nhap so dien thoai'), }))
    email_regex = RegexValidator(regex=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', message="Email khong hop le")
    email = forms.EmailField(label=_("Email"), max_length=50, widget=forms.EmailInput(
        attrs={'class': 'form-control form-control-user', 'placeholder': _('Nhap email'), }))
    username = forms.CharField(label=_("Username"), max_length=32, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-user', 'placeholder': _('Ten tai khoan'), }))
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-user', 'placeholder': _('Mat khau')}), help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-user', 'placeholder': _('Xac nhan mat khau')}), help_text=password_validation.password_validators_help_text_html())

    def clean(self):
        staff_id = self.cleaned_data.get('staff_id')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        s = Staff.objects.filter(staff_id__exact=staff_id)
        if s.count():
            st = Staff.objects.get(staff_id__exact=staff_id)
            if st.user:
                raise forms.ValidationError(
                    self.error_messages['staff_username_exists'],
                    code='staff_username_exits',
                )
            elif first_name != st.first_name or last_name != st.last_name or email != st.staff_email:
                raise forms.ValidationError(
                    self.error_messages['info_not_matched'],
                    code='info_not_matched',
                )
        else:
            raise forms.ValidationError(
                self.error_messages['id_not_found'],
                code='id_not_found',
            )

        if not re.search(r'^(?=.{8,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$', username):
            raise forms.ValidationError("Tên tài khoản có kí tự đặc biệt")

        u = User.objects.filter(username__iexact=username)
        if u.count():
            raise forms.ValidationError(
                self.error_messages['username_exists'],
                code='username_exists',
            )

        e = User.objects.filter(email__iexact=email)
        if e.count():
            raise forms.ValidationError(
                self.error_messages['email_exists'],
                code='email_exists',
            )

        if len(password1) < 8 or len(password1) > 20:
            raise forms.ValidationError(
                self.error_messages['password_length'],
                code='password_length',
            )

        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError(
                self.error_messages['password_digit'],
                code='password_digit',
            )

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

    def save(self):
        user = User.objects.create(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
        )
        return user


class PasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['old_password'].widget.attrs['placeholder'] = 'Mat khau cu'
        self.fields['old_password'].label = 'Nhap mat khau cu'

        self.fields['new_password1'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Mat khau moi'
        self.fields['new_password1'].label = 'Nhap mat khau moi'
        self.fields['new_password1'].help_text = [
            'Mật khẩu của bạn không được quá giống với thông tin cá nhân khác của bạn',
            'Mật khẩu của bạn phải chứa ít nhất 8 ký tự', 'Mật khẩu của bạn không thể là mật khẩu thường dùng',
            'Mật khẩu của bạn không được hoàn toàn là số']

        self.fields['new_password2'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Xac nhan mat khau'
        self.fields['new_password2'].label = 'Nhap mat lai khau'

        self.error_messages['password_incorrect'] = "Mật khẩu cũ của bạn đã được nhập không chính xác. Vui lòng nhập " \
                                                    "lại. "
        self.error_messages['password_mismatch'] = 'Hai trường mật khẩu không khớp.'


class ResetPasswordForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(
            attrs={'autocomplete': 'email', 'class': 'form-control form-control-user', 'placeholder': 'Nhap email'})
    )


class SetPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Mat khau moi'
        self.fields['new_password1'].label = 'Nhap mat khau moi'
        self.fields['new_password1'].help_text = [
            'Mật khẩu của bạn không được quá giống với thông tin cá nhân khác của bạn',
            'Mật khẩu của bạn phải chứa ít nhất 8 ký tự', 'Mật khẩu của bạn không thể là mật khẩu thường dùng',
            'Mật khẩu của bạn không được hoàn toàn là số']

        self.fields['new_password2'].widget.attrs['class'] = 'form-control form-control-user'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Xac nhan mat khau'
        self.fields['new_password2'].label = 'Nhap mat lai khau'

        self.error_messages['password_mismatch'] = 'Hai trường mật khẩu không khớp.'


class ProfileForm(forms.ModelForm):
    error_messages = {
        'errors_phone_number': _("So dien thoai khong hop le"),
    }

    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    quote = forms.CharField(max_length=255)

    phone_regex = RegexValidator(regex=r'^\+?\d{8,11}$', message="So dien thoai khong hop le")
    phone = forms.CharField(label=_('Contact No'), validators=[phone_regex], max_length=13,
                                 widget=forms.TextInput(attrs={'class': 'form-control form-control-user',
                                                               'placeholder': _('Nhap so dien thoai'), }))

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']


def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg