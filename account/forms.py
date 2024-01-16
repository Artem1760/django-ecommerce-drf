from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomerUser, CustomerProfile
from checkout.models import Address


class RegistrationForm(UserCreationForm):
    """
    User register form
    """

    class Meta:
        model = CustomerUser
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if CustomerUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        return username

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomerUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email


class UserEditForm(forms.ModelForm):
    """
    Form for Profile to edit account details.
    """

    email = forms.EmailField(
        label='Email Address (Can not be changed)', max_length=200,
        widget=forms.TextInput(
            attrs={'type': 'email', 'class': 'form-control',
                   'placeholder': 'email', 'id': 'form-email',
                   'readonly': 'readonly'}))

    username = forms.CharField(
        label='Username (Can not be changed)', min_length=3, max_length=50,
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control',
                   'placeholder': 'Username', 'id': 'form-username',
                   'readonly': 'readonly'}))

    first_name = forms.CharField(
        label='First Name*', min_length=2, max_length=50,
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control',
                   'placeholder': 'Firstname', 'id': 'form-firstname'}))

    last_name = forms.CharField(
        label='Last Name*', min_length=2, max_length=50,
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control',
                   'placeholder': 'Lastname', 'id': 'form-lastname'}))

    phone = forms.CharField(
        label='Phone*', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control',
                   'placeholder': 'Phone', 'id': 'form-phone'}))

    avatar = forms.ImageField(
        label='Avatar*', widget=forms.ClearableFileInput(
            attrs={'class': 'form-control', 'id': 'form-avatar'}),
        required=False)

    class Meta:
        model = CustomerProfile
        fields = ['email', 'username', 'first_name', 'last_name', 'phone',
                  'avatar']
        required_fields = ['email', 'username', 'first_name', 'last_name',
                           'phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.Meta.required_fields:
            self.fields[field_name].required = True

        # Set the initial value for the avatar field
        self.fields['avatar'].initial = self.instance.avatar


class UserAddressForm(forms.ModelForm):
    """
    Form for user address information.
    """

    class Meta:
        model = Address
        fields = (
            'first_name', 'last_name', 'email', 'country', 'country_state',
            'postcode', 'street_address', 'town_city', 'phone', 'default')
