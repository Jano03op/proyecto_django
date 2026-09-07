from django.test import TestCase, Client
from django.urls import reverse
from . import services
from datosarray import actividades


class OrganizacionDatosArrayTests(TestCase):
    def test_obtener_personas(self):
        personas = services.obtener_personas()
        self.assertGreater(len(personas), 0)
        nombres = [p['nombre'] for p in personas]
        self.assertIn('Elizabeth Villanueva', nombres)

    def test_obtener_delegaciones(self):
        delegaciones = services.obtener_delegaciones()
        self.assertIn('La Antena', delegaciones)
        self.assertIn('Centro', delegaciones)

    def test_obtener_persona_por_nombre(self):
        persona = services.obtener_persona_por_nombre('Elizabeth Villanueva')
        self.assertIsNotNone(persona)
        self.assertEqual(persona['delegacion'], 'La Antena')
        self.assertEqual(persona['cargo'], 'Delegada')
        self.assertGreater(len(persona['items']), 0)

    def test_obtener_coordinador(self):
        coordinador = services.obtener_coordinador()
        self.assertIsNotNone(coordinador)
        self.assertEqual(coordinador['cargo'], 'Coordinador')

    def test_obtener_actividades_desde_datosarray(self):
        lista = services.obtener_actividades()
        self.assertGreaterEqual(len(lista), 7)
        self.assertEqual(lista[0]['funcionario'], 'Elizabeth Villanueva')

    def test_crear_actividad(self):
        nueva = services.crear_actividad(
            fecha="2026-09-06",
            funcionario="Elizabeth Villanueva",
            delegacion="La Antena",
            item="Atención de usuario",
            descripcion="Atención de prueba",
            accion="Orientación",
            contacto="Vecino Test",
            telefono="+56912345678"
        )
        self.assertIn("EVI-ANT-", nueva["evidencia"]["codigo"])
        self.assertEqual(nueva["evidencia"]["estado"], "Pendiente")

    def test_crear_actividad_formato_dia_mes_ano(self):
        nueva = services.crear_actividad(
            fecha="07/09/2026",
            funcionario="Elizabeth Villanueva",
            delegacion="La Antena",
            item="Atención de usuario",
            descripcion="Prueba formato fecha",
            accion="Accion test",
            contacto="Contacto test",
            telefono="+56999999999"
        )
        self.assertEqual(nueva["fecha"], "2026-09-07")

    def test_actualizar_estado_evidencia(self):
        ok = services.actualizar_estado_evidencia(1, "Aprobado", observacion="Revisado OK")
        self.assertTrue(ok)
        act = services.obtener_actividad_por_id(1)
        self.assertEqual(act["evidencia"]["estado"], "Aprobado")

    def test_panel_admin_view(self):
        client = Client()
        response = client.get(reverse('panel_admin'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('delegaciones', response.context)
        self.assertIn('actividades', response.context)

    def test_panel_funcionario_view(self):
        client = Client()
        response = client.get(reverse('panel_funcionario'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('personas', response.context)
        self.assertIn('persona_info', response.context)

    def test_registrar_actividad_view_get(self):
        client = Client()
        response = client.get(reverse('registrar_actividad'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('personas', response.context)
