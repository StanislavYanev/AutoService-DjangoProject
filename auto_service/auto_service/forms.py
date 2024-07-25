from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

class CustomAuthenticationForm(AuthenticationForm):


    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})
