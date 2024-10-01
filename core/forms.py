from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .validators import *
from .models import *


class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'nombre de usuario',
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'contraseña',
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


class TicketSearchForm(forms.Form):
    q = forms.CharField(
        label='Título',
        required=False,
        min_length=3,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'por título...',
            }
        )
    )
    type = forms.ChoiceField(
        label='Tipo',
        required=False,
        choices=[('','--------')]+[(choice.value, choice.name) for choice in TicketType],
        widget=forms.Select(attrs={'class': 'form-control form-control-sm text-center'})
    )
    category = forms.ModelChoiceField(
        label='Categoría',
        required=False,
        queryset=TicketCategory.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )
    severity = forms.ChoiceField(
        label='Severidad',
        required=False,
        choices=[('','--------')]+[(choice.value, choice.name) for choice in Severity],
        widget=forms.Select(attrs={'class': 'form-control form-control-sm text-center'})
    )
    impact = forms.ChoiceField(
        label='Impacto',
        required=False,
        choices=[('','--------')]+[(choice.value, choice.name) for choice in Impact],
        widget=forms.Select(attrs={'class': 'form-control form-control-sm text-center'})
    )
    status = forms.ChoiceField(
        label='Estado',
        required=False,
        choices=[('','--------')]+[(choice.value, choice.name) for choice in TicketStatus],
        widget=forms.Select(attrs={'class': 'form-control form-control-sm text-center'})
    )
    assignedTo = forms.ModelChoiceField(
        label='Responsable',
        required=False,
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control form-control-sm text-center'})
    )


class TicketCategoryForm(forms.ModelForm):

    class Meta:
        model = TicketCategory
        fields = ['name', 'subcategory', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'minlength': 3, }),
            'subcategory': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'minlength': 3}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 4, 'minlength': 20}),
        }


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['type', 'category', 'title',
            'severity', 'impact', 'assignedTo', 'resume']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'category': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'title': forms.TextInput(attrs={'class': 'form-control form-control-sm',  'minlength': 5, }),
            'severity': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'impact': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'assignedTo': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'resume': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 4, }),
        }


class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['type', 'category', 'title', 'severity',
            'impact', 'assignedTo', 'status', 'resume']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'category': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'title': forms.TextInput(attrs={'class': 'form-control form-control-sm',  'minlength': 5, }),
            'severity': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'impact': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'assignedTo': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'status': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'resume': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 4, }),
        }


class TicketReportForm(forms.ModelForm):
    CHOICES = [('','----'),('close','Cerrar')]
    
    action = forms.ChoiceField(choices=CHOICES, required=False, label='Acción')
    class Meta:
        model = TicketReport
        fields = ['action','report']
        widgets = {
            'action': forms.Select(attrs={'class': 'form-select'}),
            'report': QuillField(blank=False),
        }