from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Property
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2', 'user_type']



class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['city', 'area', 'house_type', 'other_type', 'bedrooms', 'bathrooms', 'balcony', 'swimming_pool', 'playing_area']
        widgets = {
            'house_type': forms.Select(attrs={'id': 'house_type'}),
            'other_type': forms.TextInput(attrs={'id': 'other_type', 'style': 'display:none;'}),
        }
