from dataclasses import field, fields
from pyexpat import model
from tkinter import Widget
from turtle import width
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .validators import *
from .models import *


class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "nombre de usuario",
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "contraseña",
    }))


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'nombre de usuario',
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'pepito@correo.com',
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese una contraseña',
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repita la contraseña',
    }))

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class TicketCategoryForm(forms.ModelForm):
    
    class Meta:
        model = TicketCategory
        fields = ["category", "subcategory", "description"]
        widgets = {
            "description" : forms.Textarea(attrs={'cols':5}),
        }


class SearchForm(forms.Form):
    q = forms.CharField(
        label="search",
        required=False,
        min_length=3,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese un parametro para buscar...",
            }
        )
    )


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "type", "category", "severity", "impact", "assignedTo", "resume", "caputres"]
        widgets = {
            "resume" : forms.Textarea(attrs={'cols':5}),
            "caputres" : forms.ClearableFileInput(attrs={"multiple": True}),
        }