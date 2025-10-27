from django import forms
from django.contrib.auth.models import User
from .models import Trabajador

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cd['password2']

class TrabajadorProfileForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ('resumen_profesional', 'cv', 'habilidades')