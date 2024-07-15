from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from captcha.fields import CaptchaField


class EmailLoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField()

class CategoriaFilterForm(forms.Form):
    categoria = forms.ModelChoiceField(queryset=CateNew.objects.all(), required=True, label="Seleccione una categoría")
    
class UserFilterForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label="Nombre de usuario")


class NewForm(ModelForm):
    location = forms.CharField(required=False, label='Ubicación', max_length=200)
    captcha = CaptchaField()
    
    class Meta:
        model = New
        fields = ['titulo', 'categoria', 'texto', 'imagen1', 'imagen2', 'imagen3', 'location']


User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Nombre", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email esta en uso.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].lower()
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
        return user
    
class StaffUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Nombre", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'password1', 'password2')
        
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email esta en uso.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].lower()
        user.first_name = self.cleaned_data['first_name']
        user.is_staff = True
        if commit:
            user.save()
        return user