from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Trabajador
from Empresa.models import Empresa

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido. Ingrese un correo válido.")
    first_name = forms.CharField(max_length=150, required=True, help_text="Requerido.")
    last_name = forms.CharField(max_length=150, required=True, help_text="Requerido.")
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)
        
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

class TrabajadorProfileForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ('resumen_profesional', 'cv', 'habilidades')

class EmpresaRegistrationForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = (
            'industria', 'rut', 'razon_social', 'descripcion',
            'ubicacion_texto', 'tamano_rango', 'por_que_elegirla', 'roles_clave'
        )
