"""
    1) Lee lo que llegó en la petición (request.GET o request.POST).
    2) Le pide los datos a agenda/services.py (que es quien sabe leer y
       escribir el archivo JSON).
    3) Entrega esos datos a un template con render(), o redirige a otra
       página con redirect() cuando corresponde.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from . import services

def tablero_agenda(request):
    territorio = request.GET.get('territorio', '').strip()
    responsable = request.GET.get('responsable', '').strip()
    compromisos = services.obtener_compromisos(
        filtro_territorio=territorio if territorio else None,
        filtro_responsable=responsable if responsable else None,)


    territorios_disponibles = sorted({
        c.get("territorio") for c in services.cargar_compromisos() if c.get("territorio")})

    for compromiso in compromisos:
        compromiso["vencido"] = services.esta_vencido(compromiso)
    columnas = services.agrupar_por_estado(compromisos)
    contexto = {
        'columnas': columnas,
        'total_compromisos': len(compromisos),
        'territorio_filtro': territorio,
        'responsable_filtro': responsable,
        'territorios_disponibles': territorios_disponibles,
    }
    return render(request, 'agenda/tablero.html', contexto)

def crear_compromiso(request):
    """
    Si la petición es GET, solo se muestra el formulario vacío.
    Si la petición es POST, se valida que los campos obligatorios
    (solicitante, territorio, responsable y fecha comprometida) no
    vengan vacíos antes de guardar; si falta alguno, se vuelve a mostrar
    el formulario con un mensaje de error y sin perder lo ya escrito.
    """
    if request.method == 'POST':
        origen = request.POST.get('origen', 'Solicitud ciudadana')
        solicitante = request.POST.get('solicitante', '').strip()
        territorio = request.POST.get('territorio', '').strip()
        responsable = request.POST.get('responsable', '').strip()
        area_apoyo = request.POST.get('area_apoyo', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        fecha_compromiso = request.POST.get('fecha_compromiso', '').strip()
        campos_obligatorios = [solicitante, territorio, responsable, fecha_compromiso, descripcion]
        if not all(campos_obligatorios):
            messages.error(request, 'Debe completar solicitante, territorio, responsable, fecha y descripción.')
            return render(request, 'agenda/crear_compromiso.html', {
                'valores': request.POST,})

        usuario_sesion = request.session.get('usuario')
        autor_registro = usuario_sesion.get('nombre') if usuario_sesion else responsable

        nuevo = services.crear_compromiso(
            origen=origen,
            solicitante=solicitante,
            territorio=territorio,
            responsable=responsable,
            area_apoyo=area_apoyo,
            descripcion=descripcion,
            fecha_compromiso=fecha_compromiso,
            autor=autor_registro,
        )
        messages.success(request, f'Compromiso #{nuevo["id"]} registrado correctamente en estado "Ingresado".')
        return redirect('tablero_agenda')

    valores_iniciales = {}
    usuario_sesion = request.session.get('usuario')
    if usuario_sesion:
        valores_iniciales = {
            'responsable': usuario_sesion.get('nombre', ''),
            'territorio': usuario_sesion.get('delegacion', ''),
        }

    return render(request, 'agenda/crear_compromiso.html', {'valores': valores_iniciales})

def detalle_compromiso(request, id):
    """
    Muestra el detalle completo de un compromiso (incluido su
    historial de cambios de estado) y permite actualizar su estado
    dejando una observación obligatoria.
    """
    compromiso = services.obtener_compromiso_por_id(id)
    if compromiso is None:
        messages.error(request, 'El compromiso solicitado no existe.')
        return redirect('tablero_agenda')

    compromiso["vencido"] = services.esta_vencido(compromiso)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado', '').strip()
        observacion = request.POST.get('observacion', '').strip()
        usuario_sesion = request.session.get('usuario')
        autor_default = usuario_sesion.get('nombre') if usuario_sesion else compromiso.get('responsable', 'Delegado')
        autor = request.POST.get('autor', '').strip() or autor_default

        actualizado = services.cambiar_estado_compromiso(
            compromiso_id=id,
            nuevo_estado=nuevo_estado,
            autor=autor,
            observacion=observacion,)
        if actualizado:
            messages.success(request, f'El compromiso {id} ahora está en estado "{nuevo_estado}".')
        else:
            messages.error(request, 'No se pudo actualizar el estado del compromiso.')

        return redirect('detalle_compromiso', id=id)

    contexto = {
        'compromiso': compromiso,
        'estados': services.ESTADOS,
    }
    return render(request, 'agenda/detalle_compromiso.html', contexto)
