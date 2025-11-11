from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from .forms import UserRegistrationForm, TrabajadorProfileForm
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from .models import Trabajador, Habilidad, Certificacion

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

def employeeView(request) :
    emp = {
        'id':123,
        'name' : 'Clark',
        'email' : 'sup@jl.org',
        'salary' : '5000'
    }
    return JsonResponse (emp)

class CustomLogoutView(SuccessMessageMixin, LogoutView):
    success_message = "Has cerrado sesión exitosamente."
    next_page = reverse_lazy('login')

    # Opcional: Para permitir logout con GET (menos seguro)
    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


@login_required
def add_habilidades(request):
    if request.method != 'POST':
        return redirect('curso-list')

    habilidades_text = request.POST.get('habilidades_text', '')
    if not habilidades_text.strip():
        messages.warning(request, 'Ingresa al menos una habilidad.')
        return redirect('curso-list')

    # Normalizar separadores y dividir
    raw_items = habilidades_text.replace('\n', ',').replace(';', ',').split(',')
    nombres = [item.strip() for item in raw_items if item.strip()]

    if not nombres:
        messages.warning(request, 'No se detectaron habilidades válidas.')
        return redirect('curso-list')

    # Asegurar perfil de Trabajador
    trabajador, _ = Trabajador.objects.get_or_create(usuario=request.user)

    added = 0
    for nombre in nombres:
        if len(nombre) > 100:
            nombre = nombre[:100]
        habilidad, _ = Habilidad.objects.get_or_create(nombre_habilidad=nombre)
        trabajador.habilidades.add(habilidad)
        added += 1

    messages.success(request, f'Se añadieron {added} habilidad(es) a tu perfil.')
    return redirect('curso-list')


@login_required
def profile_update(request):
    # Crear o recuperar perfil
    perfil, _ = Trabajador.objects.get_or_create(usuario=request.user)
    if request.method != 'POST':
        return redirect('curso-list')

    # Actualización segura por campos específicos
    resumen = request.POST.get('resumen_profesional')
    certificaciones_text = request.POST.get('certificaciones_text')
    proyectos_text = request.POST.get('proyectos_text')
    idiomas_text = request.POST.get('idiomas_text')
    preferencias_text = request.POST.get('preferencias_text')

    # Validaciones: bloquear envíos vacíos por sección
    if 'resumen_profesional' in request.POST and (resumen is None or not resumen.strip()):
        messages.warning(request, 'El resumen no puede estar vacío.')
        return redirect('curso-list')
    if 'proyectos_text' in request.POST and (proyectos_text is None or not proyectos_text.strip()):
        messages.warning(request, 'Ingresa al menos un proyecto.')
        return redirect('curso-list')
    if 'idiomas_text' in request.POST and (idiomas_text is None or not idiomas_text.strip()):
        messages.warning(request, 'Ingresa al menos un idioma.')
        return redirect('curso-list')
    if 'preferencias_text' in request.POST and (preferencias_text is None or not preferencias_text.strip()):
        messages.warning(request, 'Ingresa tus preferencias de aprendizaje.')
        return redirect('curso-list')
    if 'certificaciones_text' in request.POST and (certificaciones_text is None or not certificaciones_text.strip()) and 'certificacion_file' not in request.FILES:
        messages.warning(request, 'Ingresa texto de certificación o selecciona un archivo.')
        return redirect('curso-list')

    # Partimos del resumen actual si existe
    resumen_actual = perfil.resumen_profesional or ''
    nuevo_resumen = resumen if resumen is not None else resumen_actual

    def normalize_list(text):
        items = []
        if text:
            raw = text.replace('\n', ',').replace(';', ',').split(',')
            items = [s.strip() for s in raw if s.strip()]
        return items

    certs = normalize_list(certificaciones_text)
    projs = normalize_list(proyectos_text)
    idiomas = normalize_list(idiomas_text)
    prefs = normalize_list(preferencias_text)

    blocks = []
    if certs:
        blocks.append('Certificaciones:\n' + '\n'.join(f'- {c}' for c in certs))
    if projs:
        blocks.append('Proyectos destacados:\n' + '\n'.join(f'- {p}' for p in projs))
    if idiomas:
        blocks.append('Idiomas:\n' + '\n'.join(f'- {i}' for i in idiomas))
    if prefs:
        blocks.append('Preferencias de aprendizaje:\n' + '\n'.join(f'- {pr}' for pr in prefs))

    if blocks:
        joiner = '\n\n' if nuevo_resumen else ''
        nuevo_resumen = (nuevo_resumen or '') + joiner + '\n\n'.join(blocks)

    perfil.resumen_profesional = nuevo_resumen

    if 'cv' in request.FILES:
        perfil.cv = request.FILES['cv']

    # Guardar archivo de certificación si se envía
    if 'certificacion_file' in request.FILES:
        cert_file = request.FILES['certificacion_file']
        nombre_cert = None
        # si viene texto en el mismo submit, usar el primero como nombre
        if certificaciones_text:
            first = certificaciones_text.replace('\n', ',').replace(';', ',').split(',')[0].strip()
            nombre_cert = first if first else None
        Certificacion.objects.create(trabajador=perfil, archivo=cert_file, nombre=nombre_cert or '')

    perfil.save()
    messages.success(request, 'Perfil actualizado correctamente.')
    return redirect('curso-list')


@login_required
def perfil_resumen(request):
    # Obtener o crear el perfil del trabajador
    perfil, _ = Trabajador.objects.get_or_create(usuario=request.user)

    habilidades = perfil.habilidades.all().order_by('nombre_habilidad') if perfil else []
    certificaciones = Certificacion.objects.filter(trabajador=perfil).order_by('-fecha_subida')

    # Parsear bloques del texto de resumen_profesional si existen
    resumen_lines = (perfil.resumen_profesional or '').splitlines()
    current = None
    bloques = {
        'certificaciones_text': [],
        'proyectos': [],
        'idiomas': [],
        'preferencias': [],
    }
    headers_map = {
        'Certificaciones:': 'certificaciones_text',
        'Proyectos destacados:': 'proyectos',
        'Idiomas:': 'idiomas',
        'Preferencias de aprendizaje:': 'preferencias',
    }
    for raw in resumen_lines:
        line = raw.strip()
        if line in headers_map:
            current = headers_map[line]
            continue
        if current and line.startswith('- '):
            bloques[current].append(line[2:])

    context = {
        'user_obj': request.user,
        'perfil': perfil,
        'habilidades': habilidades,
        'certificaciones': certificaciones,
        'proyectos': bloques['proyectos'],
        'idiomas': bloques['idiomas'],
        'preferencias': bloques['preferencias'],
        'certificaciones_text': bloques['certificaciones_text'],
    }
    return render(request, 'Usuario/perfil_resumen.html', context)
