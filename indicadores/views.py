from django.shortcuts import render, redirect
from datosarray import periodo, personas
import random
from datetime import datetime

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

    tiempo(periodo)
    metaesperada = periodo['Calculo']['meta']

    for persona in personas:
        for actividad in persona['items']:
            resultado = actividad['avance'] / actividad['meta'] * 100
            actividad['porcentaje'] = resultado

            if resultado >= metaesperada:
                actividad['semaforo'] = "verde"
            elif resultado >= metaesperada * 0.6:
                actividad['semaforo'] = "ambar"
            else:
                actividad['semaforo'] = "rojo"

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



    tiempo(periodo)
    metaesperada = periodo['Calculo']['meta']

    peor = []
    for actividad in hola['items']:
        meta = actividad['meta']
        avance = actividad['avance']
        resultado = avance / meta * 100

        actividad['porcentaje'] = resultado
        ponderador=actividad['ponderador']*resultado/100
        actividad['ponderado_cumplimiento'] = ponderador
        if resultado >= metaesperada:
            actividad['semaforo'] = "verde"
        elif resultado >= metaesperada * 0.6:
            actividad['semaforo'] = "ambar"
        else:
            actividad['semaforo'] = "rojo"
    
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


def tiempo(periodo):

    fechainicio=datetime.strptime(periodo['inicio'], '%Y-%m-%d')
    fechatermino=datetime.strptime(periodo['termino'], '%Y-%m-%d')
    totaldias = (fechatermino - fechainicio).days
    hoy=datetime.now()
    transcurrido=(hoy-fechainicio).days
    restante=(fechatermino-hoy).days
    meta=transcurrido/totaldias*100
    hola={
        'totaldias': totaldias,
        'transcurrido': transcurrido,
        'restante': restante,
        'meta': meta,
    }
    periodo['Calculo'] = hola
    return 

def configurar_metas(request):
    if 'persona_actual' not in request.session:
        return redirect('landing')

    nombre_guardado = request.session['persona_actual']
    hola = next(p for p in personas if p['nombre'] == nombre_guardado)
    rol_actual = hola['rol']

    if rol_actual not in ['administrador', 'coordinador']:
        return redirect('landing')

    if request.method == 'POST':
        cargo_seleccionado = request.POST.get('cargo')

        for persona in personas:
            if persona['cargo'] == cargo_seleccionado:
                for actividad in persona['items']:
                    nueva_meta = request.POST.get(f'meta_{actividad["nombre"]}')
                    nuevo_ponderador = request.POST.get(f'ponderador_{actividad["nombre"]}')
                    if nueva_meta:
                        actividad['meta'] = int(nueva_meta)
                    if nuevo_ponderador:
                        actividad['ponderador'] = int(nuevo_ponderador)

    cargos_vistos = {}
    for persona in personas:
        if persona['cargo'] not in cargos_vistos and len(persona['items']) > 0:
            cargos_vistos[persona['cargo']] = persona['items']

    return render(request, 'indicadores/configurar_metas.html', {
        'rol': rol_actual,
        'cargos_vistos': cargos_vistos,
    })