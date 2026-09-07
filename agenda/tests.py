from django.test import TestCase
from . import services
from datosarray import compromisos


class AgendaServicesTests(TestCase):
    def test_obtener_compromisos(self):
        todos = services.obtener_compromisos()
        self.assertGreaterEqual(len(todos), 1)

    def test_obtener_tablero_kanban(self):
        tablero = services.obtener_tablero_kanban()
        self.assertIn("Por Iniciar", tablero)
        self.assertIn("En Proceso", tablero)
        self.assertIn("Finalizado", tablero)

    def test_crear_y_actualizar_compromiso(self):
        nuevo = services.crear_compromiso(
            titulo="Prueba compromiso",
            descripcion="Descripción de prueba",
            funcionario="Elizabeth Villanueva",
            delegacion="La Antena",
            fecha_limite="2026-09-30",
            prioridad="Alta",
            contacto="Vecino Test"
        )
        self.assertEqual(nuevo["titulo"], "Prueba compromiso")
        self.assertEqual(nuevo["estado"], "Por Iniciar")

        actualizado = services.actualizar_estado_compromiso(nuevo["id"], "En Proceso")
        self.assertTrue(actualizado)
        compromiso_modificado = services.obtener_compromiso_por_id(nuevo["id"])
        self.assertEqual(compromiso_modificado["estado"], "En Proceso")
