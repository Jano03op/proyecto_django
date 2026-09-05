from django.shortcuts import render, redirect
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
        'filtro_delegacion': delegacion,
        'filtro_estado': estado,
        'filtro_funcionario': funcionario,
    }
    return render(request, 'organizacion/panel_admin.html', context)


def panel_funcionario(request):
    """Muestra solo las actividades del funcionario actual (por defecto Elizabeth Villanueva)."""
    funcionario_actual = request.GET.get('funcionario', 'Elizabeth Villanueva')
    actividades = services.obtener_actividades(filtro_funcionario=funcionario_actual)

    context = {
        'funcionario_actual': funcionario_actual,
        'actividades': actividades,
    }
    return render(request, 'organizacion/panel_funcionario.html', context)


def registrar_actividad(request):
    """Formulario para agregar una nueva actividad y persistirla en el archivo JSON."""
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        funcionario = request.POST.get('funcionario')
        delegacion = request.POST.get('delegacion')
        item = request.POST.get('item')
        descripcion = request.POST.get('descripcion')
        accion = request.POST.get('accion')
        contacto = request.POST.get('contacto')
        telefono = request.POST.get('telefono')

        if not (fecha and funcionario and delegacion and item and descripcion):
            messages.error(request, 'Por favor, complete todos los campos obligatorios.')
            return render(request, 'organizacion/registrar_actividad.html')

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
        return redirect('panel_funcionario')

    return render(request, 'organizacion/registrar_actividad.html')


def validar_evidencia(request, id):
    """Permite a la coordinación revisar, aprobar o rechazar una evidencia."""
    actividad = services.obtener_actividad_por_id(id)
    if not actividad:
        messages.error(request, 'Actividad no encontrada.')
        return redirect('panel_admin')

    if request.method == 'POST':
        decision = request.POST.get('decision')
        observacion = request.POST.get('observacion', '').strip()
        verificador = request.POST.get('verificador', 'Alan Von Kretschmann')

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
    }
    return render(request, 'organizacion/validar_evidencia.html', context)
