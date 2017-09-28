from django import forms

class Logowanie(forms.Form):
    login = forms.CharField(label='Login', max_length=100)
    haslo = forms.CharField(label='Haslo', widget=forms.PasswordInput())