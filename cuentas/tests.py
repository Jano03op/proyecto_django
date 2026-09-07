from django.test import TestCase
from . import services
from datosarray import usuarios


class CuentasServicesTests(TestCase):
    def test_obtener_usuarios(self):
        lista = services.obtener_usuarios()
        self.assertGreaterEqual(len(lista), 1)

    def test_autenticar_usuario_exitoso(self):
        usuario = services.autenticar_usuario("evillanueva", "password123")
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario["nombre"], "Elizabeth Villanueva")

    def test_autenticar_usuario_fallido(self):
        usuario = services.autenticar_usuario("evillanueva", "wrong_pass")
        self.assertIsNone(usuario)

    def test_registrar_y_cambiar_password(self):
        nuevo = services.registrar_usuario(
            username="testuser",
            nombre="Usuario Test",
            email="test@laserena.cl",
            rol="Encargado",
            delegacion="Centro",
            password="pass"
        )
        self.assertIsNotNone(nuevo)
        self.assertEqual(nuevo["username"], "testuser")

        cambiado = services.cambiar_password("testuser", "nueva_clave")
        self.assertTrue(cambiado)
        usuario_auth = services.autenticar_usuario("testuser", "nueva_clave")
        self.assertIsNotNone(usuario_auth)
