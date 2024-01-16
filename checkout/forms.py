from django import forms

from .models import Address


class AddressForm(forms.ModelForm):
    """
    Address Form for shipping
    """

    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'phone', 'email', 'postcode',
                  'country', 'street_address', 'town_city', 'country_state',
                  'delivery_instructions']
