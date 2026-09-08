from django.shortcuts import render, redirect
from django.contrib import messages
from . import services
from agenda import services as agenda_services

def login_view(request):
    """
    Gestiona el inicio de sesión del usuario.
    Si ya hay sesión activa, redirige al inicio interno.
    Valida credenciales contra data/usuarios.json.
    """
    if request.session.get('usuario'):
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, 'Por favor ingrese su usuario y contraseña.')
            return render(request, 'cuentas/login.html', {'username': username})

        usuario = services.autenticar_usuario(username, password)
        if usuario:
            request.session['usuario'] = usuario
            messages.success(request, f'¡Bienvenido(a), {usuario["nombre"]}!')
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos. Verifique sus datos.')
            return render(request, 'cuentas/login.html', {'username': username})

    usuarios_demo = services.cargar_usuarios()
    return render(request, 'cuentas/login.html', {'usuarios_demo': usuarios_demo})


def logout_view(request):
    """
    Cierra la sesión del usuario y redirige al login.
    """
    nombre = request.session.get('usuario', {}).get('nombre', '')
    request.session.flush()
    if nombre:
        messages.info(request, f'Sesión de {nombre} cerrada exitosamente.')
    else:
        messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')


def home_view(request):
    """
    Pantalla base / Escritorio principal del sistema tras iniciar sesión.
    Muestra accesos a Agenda, Organización e Indicadores según el usuario logueado.
    """
    usuario = request.session.get('usuario')
    if not usuario:
        messages.warning(request, 'Debes iniciar sesión para acceder al sistema.')
        return redirect('login')

    compromisos = agenda_services.cargar_compromisos()
    total_compromisos = len(compromisos)
    pendientes = len([c for c in compromisos if c.get('estado') in ['Ingresado', 'Pendiente']])
    en_proceso = len([c for c in compromisos if c.get('estado') == 'En proceso'])
    realizados = len([c for c in compromisos if c.get('estado') == 'Realizado'])
    
    mis_compromisos = [c for c in compromisos if usuario['nombre'].lower() in c.get('responsable', '').lower()]

    contexto = {
        'usuario': usuario,
        'total_compromisos': total_compromisos,
        'pendientes': pendientes,
        'en_proceso': en_proceso,
        'realizados': realizados,
        'mis_compromisos': mis_compromisos[:5], 
    }
    return render(request, 'cuentas/home.html', contexto)


def registro_view(request):
    """
    Permite registrar un nuevo funcionario en data/usuarios.json.
    """
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        nombre = request.POST.get('nombre', '').strip()
        cargo = request.POST.get('cargo', 'Funcionario').strip()
        rol = request.POST.get('rol', 'Funcionario').strip()
        delegacion = request.POST.get('delegacion', '').strip()
        email = request.POST.get('email', '').strip()

        if not all([username, password, nombre, delegacion]):
            messages.error(request, 'Complete los campos obligatorios.')
            return render(request, 'cuentas/registro.html', {'valores': request.POST})

        nuevo_usuario, error = services.registrar_usuario(
            username=username,
            password=password,
            nombre=nombre,
            cargo=cargo,
            rol=rol,
            delegacion=delegacion,
            email=email
        )
        if error:
            messages.error(request, error)
            return render(request, 'cuentas/registro.html', {'valores': request.POST})

        messages.success(request, f'Usuario {username} creado con éxito. Ahora puedes iniciar sesión.')
        return redirect('login')

    return render(request, 'cuentas/registro.html', {})
