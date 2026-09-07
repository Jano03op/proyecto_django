from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from . import services

def panel_admin(request):
    """Muestra todas las actividades con filtros opcionales de delegación y estado."""
    delegacion = request.GET.get('delegacion', '').strip()
    estado = request.GET.get('estado', '').strip()
    funcionario = request.GET.get('funcionario', '').strip()

    actividades = services.obtener_actividades(
        filtro_delegacion=delegacion if delegacion else None,
        filtro_estado=estado if estado else None,
        filtro_funcionario=funcionario if funcionario else None
    )

    context = {
        'actividades': actividades,
        'delegaciones': services.obtener_delegaciones(),
        'filtro_delegacion': delegacion,
        'filtro_estado': estado,
        'filtro_funcionario': funcionario,
    }
    return render(request, 'organizacion/panel_admin.html', context)


def panel_funcionario(request):
    """Muestra solo las actividades del funcionario actual (por defecto Elizabeth Villanueva)."""
    personas = services.obtener_personas()
    nombres_disponibles = [p.get('nombre') for p in personas]

    funcionario_actual = request.GET.get('funcionario', '').strip()
    if not funcionario_actual or funcionario_actual not in nombres_disponibles:
        funcionario_actual = personas[0]['nombre'] if personas else 'Elizabeth Villanueva'

    persona_info = services.obtener_persona_por_nombre(funcionario_actual)
    actividades = services.obtener_actividades(filtro_funcionario=funcionario_actual)

    context = {
        'personas': personas,
        'funcionario_actual': funcionario_actual,
        'persona_info': persona_info,
        'actividades': actividades,
    }
    return render(request, 'organizacion/panel_funcionario.html', context)


def registrar_actividad(request):
    """Formulario para agregar una nueva actividad y persistirla en el archivo JSON."""
    personas = services.obtener_personas()

    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        funcionario = request.POST.get('funcionario')
        delegacion = request.POST.get('delegacion')
        item = request.POST.get('item')
        descripcion = request.POST.get('descripcion')
        accion = request.POST.get('accion')
        contacto = request.POST.get('contacto')
        telefono = request.POST.get('telefono')

        if not (fecha and funcionario and delegacion and item and descripcion and accion):
            messages.error(request, 'Por favor, complete todos los campos obligatorios.')
            return render(request, 'organizacion/registrar_actividad.html', {
                'personas': personas,
                'funcionario_seleccionado': funcionario,
            })

        nueva_act = services.crear_actividad(
            fecha=fecha,
            funcionario=funcionario,
            delegacion=delegacion,
            item=item,
            descripcion=descripcion,
            accion=accion,
            contacto=contacto,
            telefono=telefono
        )
        messages.success(request, f'Actividad registrada exitosamente. Código de evidencia: {nueva_act["evidencia"]["codigo"]}')
        return redirect(f"{reverse('panel_funcionario')}?funcionario={funcionario}")

    funcionario_seleccionado = request.GET.get('funcionario', '').strip()

    context = {
        'personas': personas,
        'funcionario_seleccionado': funcionario_seleccionado,
    }
    return render(request, 'organizacion/registrar_actividad.html', context)


def validar_evidencia(request, id):
    """Permite a la coordinación revisar, aprobar o rechazar una evidencia."""
    actividad = services.obtener_actividad_por_id(id)
    if not actividad:
        messages.error(request, 'Actividad no encontrada.')
        return redirect('panel_admin')

    coordinador = services.obtener_coordinador()
    verificador_defecto = f"{coordinador['nombre']} ({coordinador['cargo']})" if coordinador else "Alan Von Kretschmann (Coordinador)"

    if request.method == 'POST':
        decision = request.POST.get('decision')
        observacion = request.POST.get('observacion', '').strip()
        verificador = request.POST.get('verificador', verificador_defecto)

        if decision in ['Aprobado', 'Rechazado']:
            services.actualizar_estado_evidencia(
                actividad_id=id,
                nuevo_estado=decision,
                observacion=observacion,
                verificador=verificador
            )
            messages.success(request, f'Evidencia de la actividad #{id} actualizada a: {decision}.')
            return redirect('panel_admin')

    context = {
        'actividad': actividad,
        'verificador_defecto': verificador_defecto,
    }
    return render(request, 'organizacion/validar_evidencia.html', context)

