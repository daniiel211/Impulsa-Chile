from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib import messages, auth
from .forms import UserRegistrationForm, TrabajadorProfileForm
from .forms import EmpresaRegistrationForm
from Empresa.models import Empresa
from Empresa.models import Industria
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .models import Trabajador, Habilidad, Certificacion
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests


def register_choice(request):
    return render(request, 'Usuario/register_choice.html')

def trabajador_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = TrabajadorProfileForm(request.POST, request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            # Guardar el usuario. El método save() de UserCreationForm se encarga de la contraseña.
            new_user = user_form.save()
            
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

def empresa_register(request):
    # Semillas de industrias si no existen
    if not Industria.objects.exists():
        for nombre in [
            'Tecnología', 'Salud', 'Educación', 'Retail', 'Manufactura',
            'Agroindustria', 'Finanzas', 'Construcción', 'Servicios Profesionales', 'Logística'
        ]:
            Industria.objects.get_or_create(nombre_industria=nombre)

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        empresa_form = EmpresaRegistrationForm(request.POST)

        if user_form.is_valid() and empresa_form.is_valid():
            # Guardar el usuario usando el método save() del formulario
            new_user = user_form.save()

            empresa = empresa_form.save(commit=False)
            empresa.usuario = new_user
            empresa.save()

            messages.success(request, '¡Tu empresa fue registrada exitosamente! Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        empresa_form = EmpresaRegistrationForm()
    return render(request, 'Usuario/register_empresa.html', {'user_form': user_form, 'empresa_form': empresa_form})

def employeeView(request) :
    emp = {
        'id':123,
        'name' : 'Clark',
        'email' : 'sup@jl.org',
        'salary' : '5000'
    }
    return JsonResponse (emp)

class CustomLoginView(LoginView):
    template_name = 'Usuario/login.html'

    def form_valid(self, form):
        # Llama al método original para loguear al usuario
        response = super().form_valid(form)
        
        # Si el checkbox "remember_me" está marcado, la sesión no expira al cerrar el navegador.
        if not self.request.POST.get('remember_me', None):
            self.request.session.set_expiry(0) # Expira al cerrar el navegador
        return response

class CustomLogoutView(SuccessMessageMixin, LogoutView):
    success_message = "Has cerrado sesión exitosamente."
    next_page = reverse_lazy('login') # Esta propiedad es usada por get_redirect_url()
    http_method_names = ["get", "post"] # Permitir explícitamente peticiones GET y POST

    # Sobrescribimos el método 'get' para permitir el logout a través de un enlace (petición GET).
    # Esto es menos seguro que usar POST, pero es muy común por conveniencia.
    def get(self, request, *args, **kwargs):
        # 1. Llama a la función de logout de Django para limpiar la sesión.
        logout(request)
        # 2. Añade el mensaje de éxito que se mostrará en la siguiente página.
        messages.success(self.request, self.success_message)
        # 3. Redirige explícitamente a la URL de 'login'.
        # Esto es más seguro que depender de self.next_page, que causaba el error.
        return redirect('login')

@csrf_exempt
def google_login(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body)
        token = data.get('token')

        # Verifica el token con Google
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)

        # Extrae la información del usuario
        user_email = idinfo['email']
        user_first_name = idinfo.get('given_name', '')
        user_last_name = idinfo.get('family_name', '')

        # Busca o crea el usuario en Django
        user, created = User.objects.get_or_create(email=user_email, defaults={
            'username': user_email, # Usamos el email como username por simplicidad
            'first_name': user_first_name,
            'last_name': user_last_name,
        })

        # Inicia sesión con el backend de Django
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return JsonResponse({'success': True, 'redirect_url': reverse('curso-list')})

    except (ValueError, json.JSONDecodeError):
        return JsonResponse({'error': 'Solicitud inválida'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Error de autenticación: {str(e)}'}, status=401)


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
    if request.method != 'POST':
        # Redirigir si no es una petición POST
        return redirect('curso-list')

    # Obtener o crear el perfil del trabajador para asegurar que exista
    trabajador, _ = Trabajador.objects.get_or_create(usuario=request.user)
    form_type = request.POST.get('form_type')

    if form_type == 'resumen':
        resumen = request.POST.get('resumen_profesional', '').strip()
        if not resumen:
            messages.warning(request, 'El resumen no puede estar vacío.')
        else:
            trabajador.resumen_profesional = resumen
            trabajador.save()
            messages.success(request, 'Resumen profesional actualizado.')

    elif form_type == 'cv':
        if 'cv' not in request.FILES:
            messages.warning(request, 'Debes seleccionar un archivo PDF para tu CV.')
        else:
            trabajador.cv = request.FILES['cv']
            trabajador.save()
            messages.success(request, 'CV actualizado correctamente.')

    elif form_type == 'certificacion':
        cert_text = request.POST.get('certificaciones_text', '').strip()
        cert_file = request.FILES.get('certificacion_file')
        if not cert_text and not cert_file:
            messages.warning(request, 'Debes añadir un nombre o un archivo para la certificación.')
        else:
            # Usar la primera línea del texto como nombre si existe
            nombre_cert = cert_text.splitlines()[0].strip() if cert_text else "Certificación sin nombre"
            Certificacion.objects.create(
                trabajador=trabajador,
                nombre=nombre_cert,
                archivo=cert_file
            )
            messages.success(request, 'Certificación añadida a tu perfil.')

    # Los siguientes campos se guardan en el resumen, pero de forma más estructurada.
    # Podrías considerar crear modelos separados para ellos en el futuro.
    elif form_type == 'proyectos':
        proyectos = request.POST.get('proyectos_text', '').strip()
        if not proyectos:
            messages.warning(request, 'Ingresa al menos un proyecto.')
        else:
            # Aquí podrías guardarlo en un campo específico si lo tuvieras
            # Por ahora, lo añadimos al resumen
            # Código corregido (compatible con Python 3.11)
            trabajador.resumen_profesional = (trabajador.resumen_profesional or '') + "\n\nProyectos destacados:\n- " + proyectos.replace(',', '\n- ')
            trabajador.save()
            messages.success(request, 'Proyectos añadidos al perfil.')

    elif form_type == 'idiomas':
        idiomas = request.POST.get('idiomas_text', '').strip()
        if not idiomas:
            messages.warning(request, 'Ingresa al menos un idioma.')
        else:
            idiomas_formatted = idiomas.replace(',', '\n- ')
            trabajador.resumen_profesional = (trabajador.resumen_profesional or '') + f"\n\nIdiomas:\n- {idiomas_formatted}"
            trabajador.save()
            messages.success(request, 'Idiomas añadidos al perfil.')

    elif form_type == 'preferencias':
        preferencias = request.POST.get('preferencias_text', '').strip()
        if not preferencias:
            messages.warning(request, 'Ingresa tus preferencias de aprendizaje.')
        else:
            preferencias_formatted = preferencias.replace(',', '\n- ')
            trabajador.resumen_profesional = (trabajador.resumen_profesional or '') + f"\n\nPreferencias de aprendizaje:\n- {preferencias_formatted}"
            trabajador.save()
            messages.success(request, 'Preferencias de aprendizaje guardadas.')

    else:
        messages.error(request, 'Hubo un error al procesar el formulario. Inténtalo de nuevo.')

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
