from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['guest_name', 'guest_email']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


        if self.user and self.user.is_authenticated:
            self.fields['guest_name'].required=False
            self.fields['guest_email'].required=False
            self.fields['guest_name'].widget= forms.HiddenInput()
            self.fields['guest_email'].widget= forms.HiddenInput()
        else:
            self.fields['guest_name'].required=True
            self.fields['guest_email'].required=True

    def clean(self):
        cleaned_data = super().clean()

        if not self.user or not self.user.is_authenticated:
            name = cleaned_data.get('guest_name')
            email = cleaned_data.get('guest_email')

            if not name or not email:
                raise forms.ValidationError('Name and email are required for guest bookings')

        return cleaned_data