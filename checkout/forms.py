# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=undefined-variable,line-too-long
from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number', 'street_address1',
                  'street_address2', 'town_or_city', 'postcode', 'country',
                  'county',)

    def __init__(self, *args, **kwargs):  # noqa: F821
        """
        Add placeholders and classes, remove auto-generated labels and set
        autofocus on first field
        """

        # Calls the default init method to set up the default form
        super().__init__(*args, **kwargs)
        # Sets some placeholders for the form fields
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State, Locality',
        }

        # Sets autofocus to full name field (the first one) ensuring the
        # cursor always starts here
        self.fields['full_name'].widget.attrs['autofocus'] = True  # noqa: F821,E501
        for field in self.fields:  # noqa: F821
            if field != 'country':
                # Sets placeholder text with an asterisk if it is a required
                # field or without one if not
                if self.fields[field].required:  # noqa: F821
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                # Then sets the field to display placeholder from above dictionary  # noqa: E501
                self.fields[field].widget.attrs['placeholder'] = placeholder  # noqa: F821,E501
            # Sets up a class we'll use with css later
            self.fields[field].widget.attrs['class'] = 'stripe style-input'  # noqa: F821,E501
            # Removes labels as placeholders have already been set
            self.fields[field].label = False  # noqa: F821
