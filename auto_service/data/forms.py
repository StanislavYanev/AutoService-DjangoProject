from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    SKILL_CHOICES = {
        "Technical Knowledge": "Technical Knowledge",
        "Diagnostic Skills": "Diagnostic Skills",
        "Problem-Solving": "Problem Solving",
        "Attention to Detail": "Attention to Detail",
        "Physical Stamina": "Physical Stamina",
        "Time Management": "Time Management",
        "Communication Skills": "Communication Skills",
        "Customer Service": "Customer Service",
        "Safety Awareness": "Safety Awareness",
        "Use of Technology": "Use of Technology",
        "Teamwork": "Teamwork",
        "Organizational Skills": "Organizational Skills",
    }

    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    start_date = forms.DateField(required=True, widget=AdminDateWidget())

    skills = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple, choices=SKILL_CHOICES.items())
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    is_manager = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    is_teamleader = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = (
            "username", "email", "first_name", "last_name", "password1", "password2", "skills", "description",
            "start_date")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.skills = self.cleaned_data["skills"]
        user.description = self.cleaned_data["description"]
        user.start_date = self.cleaned_data["start_date"]
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    skills = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control'}))
    is_manager = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
    is_teamleader = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password", "skills", "description", "is_manager")
