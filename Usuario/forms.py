from django import forms
from django.contrib.auth.models import User
from .models import Trabajador

class UserRegistrationForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario", max_length=150)
    email = forms.EmailField(label="Correo electrónico")
    first_name = forms.CharField(label="Nombre", max_length=150)
    last_name = forms.CharField(label="Apellido", max_length=150)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cd['password2']
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

class TrabajadorProfileForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ('resumen_profesional', 'cv', 'habilidades')