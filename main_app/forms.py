from django import forms
from .models import Booking, StylistProfile
from django.contrib.auth.models import User



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

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }


class StylistProfileForm(forms.ModelForm):
    class Meta:
        model = StylistProfile
        fields = [
            'bio',
            'instagram',
            'facebook',
            'other',
            'profile_picture',
            'specialties',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell clients about yourself...'}),
            'instagram': forms.URLInput(attrs={'placeholder': 'Instagram URL'}),
            'facebook': forms.URLInput(attrs={'placeholder': 'Facebook URL'}),
            'other': forms.URLInput(attrs={'placeholder': 'Website or other link'}),
            'specialties': forms.TextInput(attrs={'placeholder': 'e.g. Balayage, Braids, Extensions'}),
        }

