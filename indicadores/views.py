from django.shortcuts import render, redirect
from datosarray import periodo, personas
import random


def landing(request):
    if 'persona_actual' not in request.session:
        hola = random.choice(personas)
        request.session['persona_actual'] = hola['nombre']
    else:
        nombre_guardado = request.session['persona_actual']
        hola = next(p for p in personas if p['nombre'] == nombre_guardado)

    rol_actual = hola['rol']

    if rol_actual in ['delegado', 'coordinador', 'administrador']:
        resumen_equipo = []
        for persona in personas:
            if len(persona['items']) == 0:
                continue

            porcentajes = []
            for item in persona['items']:
                porcentajes.append(item['avance'] / item['meta'] * 100)
            promedio = sum(porcentajes) / len(porcentajes)
            resumen_equipo.append({
                'nombre': persona['nombre'],
                'cargo': persona['cargo'],
                'delegacion': persona['delegacion'],
                'promedio': promedio,
            })

        resumen_equipo.sort(key=lambda x: x['promedio'])
        peores_del_equipo = resumen_equipo[:3]

        return render(request, 'indicadores/landing_monitor.html', {
            'simulacion': hola,
            'peores_del_equipo': peores_del_equipo,
            'rol': rol_actual,
        })
    else:
        peor = []
        for actividad in hola['items']:
            meta = actividad['meta']
            avance = actividad['avance']
            resultado = avance / meta * 100
            actividad['porcentaje'] = resultado
            peor.append(actividad)
        peor.sort(key=lambda x: x['porcentaje'])

        return render(request, 'indicadores/landinginterno.html', {
            'simulacion': hola,
            'actividades': peor,
            'rol': rol_actual,
        })


def dashboard(request):
    if 'persona_actual' not in request.session:
        return redirect('landing')

    nombre_guardado = request.session['persona_actual']
    hola = next(p for p in personas if p['nombre'] == nombre_guardado)
    rol_actual = hola['rol']

    return render(request, 'indicadores/dashboard.html', {
        'periodo': periodo,
        'personas': personas,
        'rol': rol_actual,
    })


def logueo(request):
    if 'persona_actual' not in request.session:
        return redirect('landing')

    nombre_guardado = request.session['persona_actual']
    hola = next(p for p in personas if p['nombre'] == nombre_guardado)
    rol_actual = hola['rol']

    peor = []
    for actividad in hola['items']:
        meta = actividad['meta']
        avance = actividad['avance']
        resultado = avance / meta * 100
        actividad['porcentaje'] = resultado
        peor.append(actividad)
    peor.sort(key=lambda x: x['porcentaje'])

    return render(request, 'indicadores/indicador.html', {
        'simulacion': hola,
        'rol': rol_actual,
    })


def resetear(request):
    request.session.flush()
    return redirect('landing')


def mi_cuenta(request):
    if 'persona_actual' not in request.session:
        return redirect('landing')

    nombre_guardado = request.session['persona_actual']
    hola = next(p for p in personas if p['nombre'] == nombre_guardado)

    inicial = hola['nombre'][0]
    rol_actual = hola['rol']

    return render(request, 'indicadores/mi_cuenta.html', {
        'simulacion': hola,
        'inicial': inicial,
        'rol': rol_actual,
    })