from django.contrib.auth.models import User
from .models import *
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserInfo
        fields = ['name', 'age', 'email', 'college']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name'}),
            'age': forms.NumberInput(attrs={'class':'form-control', 'min': 1, 'placeholder':'Age'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
            'college': forms.TextInput(attrs={'class':'form-control','placeholder':'College'}),
        }
