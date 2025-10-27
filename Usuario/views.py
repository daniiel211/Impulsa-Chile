from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, TrabajadorProfileForm

def trabajador_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = TrabajadorProfileForm(request.POST, request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            # Crear el objeto User pero no guardarlo en la base de datos todavía
            new_user = user_form.save(commit=False)
            # Establecer la contraseña elegida
            new_user.set_password(user_form.cleaned_data['password'])
            # Guardar el objeto User
            new_user.save()
            
            # Crear el perfil del trabajador
            profile = profile_form.save(commit=False)
            profile.usuario = new_user
            profile.save()
            # Guardar las relaciones ManyToMany
            profile_form.save_m2m()
            
            messages.success(request, '¡Tu cuenta ha sido creada exitosamente! Ya puedes iniciar sesión.')
            return redirect('login') # Asumiendo que tendrás una URL para login
    else:
        user_form = UserRegistrationForm()
        profile_form = TrabajadorProfileForm()
    return render(request, 'Usuario/register.html', {'user_form': user_form, 'profile_form': profile_form})