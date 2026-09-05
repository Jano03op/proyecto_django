from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import DelegacionForm
from .models import Delegacion

PER_PAGE = 5


def delegaciones_list(request):
    """Listado de delegaciones: búsqueda por nombre/ámbito + filtro de estado + paginación."""
    search = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', 'Todas')

    delegaciones = Delegacion.objects.all()
    if search:
        delegaciones = delegaciones.filter(
            Q(nombre__icontains=search) | Q(ambito__icontains=search)
        )
    if estado in ('Activa', 'Inactiva'):
        delegaciones = delegaciones.filter(estado=estado)

    paginator = Paginator(delegaciones, PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))

    contexto = {
        'page_obj': page_obj,
        'search': search,
        'estado': estado,
        'total': delegaciones.count(),
    }
    return render(request, 'organizacion/delegacion_list.html', contexto)


def delegacion_create(request):
    if request.method == 'POST':
        form = DelegacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Delegación creada correctamente.')
            return redirect('organizacion:delegaciones_list')
    else:
        form = DelegacionForm()
    return render(request, 'organizacion/delegacion_form.html', {'form': form, 'editing': False})


def delegacion_edit(request, pk):
    delegacion = get_object_or_404(Delegacion, pk=pk)
    if request.method == 'POST':
        form = DelegacionForm(request.POST, instance=delegacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cambios guardados correctamente.')
            return redirect('organizacion:delegaciones_list')
    else:
        form = DelegacionForm(instance=delegacion)
    return render(request, 'organizacion/delegacion_form.html', {
        'form': form, 'editing': True, 'delegacion': delegacion,
    })


def delegacion_detail(request, pk):
    delegacion = get_object_or_404(Delegacion, pk=pk)
    funcionarios = delegacion.funcionarios.select_related('cargo').all()
    return render(request, 'organizacion/delegacion_detail.html', {
        'delegacion': delegacion,
        'funcionarios': funcionarios,
    })


@require_POST
def delegacion_toggle_estado(request, pk):
    """Activa/desactiva una delegación. No elimina historial ni funcionarios asociados."""
    delegacion = get_object_or_404(Delegacion, pk=pk)
    if delegacion.estado == Delegacion.Estado.ACTIVA:
        delegacion.estado = Delegacion.Estado.INACTIVA
        mensaje = f'Delegación "{delegacion.nombre}" desactivada.'
    else:
        delegacion.estado = Delegacion.Estado.ACTIVA
        mensaje = f'Delegación "{delegacion.nombre}" activada.'
    delegacion.save(update_fields=['estado', 'actualizado'])
    messages.success(request, mensaje)

    siguiente = request.POST.get('next')
    if siguiente:
        return redirect(siguiente)
    return redirect('organizacion:delegaciones_list')
