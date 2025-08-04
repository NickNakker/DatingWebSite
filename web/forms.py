from django import forms
from .models import Profile
from django.contrib.auth.models import User
from datetime import date

class UserProfile(forms.ModelForm):
    birth_date = forms.DateField(
        label='Дата рождения',
        initial=format(date.today()),
        required= True,
        widget=forms.widgets.DateInput(attrs={'type': 'date'})
        )
    name = forms.CharField(required=True)
    location = forms.CharField(required=True)

    class Meta:
        model = Profile
        fields = ['biografy', 'location', 'birth_date' , 'photo', 'name']

class UserRegistration(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'username']