from django.test import TestCase, Client
from APPWapiptda.models import *
from APPWapiptda.factories import *
from django.contrib.auth.models import User
from APPWapiptda.views import *
from django.urls import reverse

# API
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token

# Eliminacion y modificación de registro


class TestGradoTDAHInstancia(APITestCase):
    def setUp(self):
        self.cliente = Client()
        self.user = UserFactory.create()
        self.usuario = UsuarioFactory.create(user=self.user)
        self.grado = GradoFactory.create()

    # Autenticación del cliente
    def get_authenticated_client(self, user):
        client = APIClient()
        client.force_authenticate(user=user)
        return client
    
    # Eliminación de registro de TDA
    def test_eliminar_grado(self):
        print("Eliminación de registro de tdah")
        # Obtener un cliente autenticado como usuario técnico
        client = self.get_authenticated_client(self.user)
        # Obtener la URL para eliminar el grado de tdah actual
        url = reverse('grado-detail', kwargs={'pk': self.grado.id})
        # Hacer una solicitud DELETE
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Verificar que el grado de tdah fue eliminado
        with self.assertRaises(GradoTDAH.DoesNotExist):
            self.grado.refresh_from_db()

    # Modificación de registro de TDAH
    def test_modificar_grado(self):
        print("Modificación de registro de tdah")
        # Obtener un cliente autenticado como usuario técnico
        client = self.get_authenticated_client(self.user)
        # Obtener la URL para modificar el registro de nivel de tdah
        url = reverse('grado-detail', kwargs={'pk': self.grado.id})
        # Nuevos datos para la modificación
        nuevos_datos = {
            'nombre_nivel': 'NuevoNombre',
            'descripcion_grado': 'NuevaDescripcion',
        }
        # Hacer una solicitud PUT
        response = client.put(url, data=nuevos_datos, format='json')
        # Verificar la respuesta
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


""" 
    def get_authenticated_client(self, user):
        # Autenticar un cliente con un usuario específico
        client = APIClient()
        client.force_authenticate(user=user)
        return client

    def test_modificar_usuario_comun(self):
        print("Modificación")
        # Obtener un cliente autenticado como usuario común
        client = self.get_authenticated_client(self.user)

        # Obtener la URL para modificar el usuario común actual
        url = reverse('comun-detail', kwargs={'pk': self.usuariocomun.id})
        # Nuevos datos para la modificación
        nuevos_datos = {
            'nombre_usuario': 'NuevoNombre',
            'apellido_usuario': 'NuevoApellido',
            # Agrega otros campos que deseas modificar
        }
        # Hacer una solicitud PUT a la vista de modificación proporcionada por el conjunto de vistas
        response = client.put(url, data=nuevos_datos, format='json')
        # Verificar la respuesta
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_eliminar_usuario_comun(self):
        # Obtener un cliente autenticado como usuario común
        client = self.get_authenticated_client(self.user)
        # Obtener la URL para eliminar el usuario común actual
        url = reverse('user-detail', kwargs={'pk': self.usuariocomun.user.id})
        # Hacer una solicitud DELETE a la vista de eliminación proporcionada por
        # el conjunto de vistas
        response = client.delete(url)
        # Verificar la respuesta
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Verificar que el usuario común fue eliminado
        with self.assertRaises(User.DoesNotExist):
            self.usuariocomun.user.refresh_from_db()
"""


"""
class TestDatosUsuario(APITestCase):
    def setUp(self):
        self.cliente = Client()
        self.user = UserFactory.create()
        self.usuariocomun = UsuarioComunFactory.create(user=self.user)

        self.client = APIClient()

    def get_authenticated_client(self, user):
        # Autenticar un cliente con un usuario específico y agregar el token al cliente
        client = APIClient()
        token, _ = Token.objects.get_or_create(user=user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        return client

    def test_datos_usuario_tecnico(self):
        self.user.set_password('1234')
        self.user.save()
        response = self.cliente.login(
            username=self.usuariocomun.username_usuario, password='1234')
        self.assertEqual(response, True)
    
        token = Token.objects.get(user=self.user)

        # Obtener un cliente autenticado como técnico con el token JWT
        client = self.get_authenticated_client(self.user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Hacer una solicitud GET a la vista
        response = client.get('/wapiptdah/datos/usuario/')

        # Verificar la respuesta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], True)
    """

""" 
    def test_datos_usuario_no_autenticado(self):
        # No autenticar

        # Hacer una solicitud GET a la vista
        response = self.client.get('/ruta_de_tu_vista/')

        # Verificar la respuesta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], False)
    """


"""
class UsuariosTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario_comun = UsuarioComunFactory.create()
        self.user = UserFactory.create()

    def test_usuario_comun_creation(self):
        self.assertEqual(self.usuario_comun.nombre_usuario, "Maria")
        self.assertEqual(self.usuario_comun.is_activo, False)
        self.assertEqual(self.usuario_comun.is_comun, True)
    
    def test_usuario_comun_login(self):
        self.user.set_password('1234')
        self.user.save()
        response = self.client.login(username=self.usuario_comun.username_usuario, password='1234')
        self.assertEqual(response, True)
"""

""" 
class UsuariosTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario_comun = UsuarioComunFactory.create()
        self.usuario = UsuarioFactory.create()
        self.paciente = PacienteFactory.create()
        self.user = UserFactory.create()

    def test_usuario_comun_creation(self):
        self.assertEqual(self.usuario_comun.nombre_usuario, "Maria")
        self.assertEqual(self.usuario_comun.is_activo, False)
        self.assertEqual(self.usuario_comun.is_comun, True)
    
    def test_usuario_creation(self):
        self.assertEqual(self.usuario.nombre_usuario, "Juan")
        self.assertEqual(self.usuario.is_activo, False)
        self.assertEqual(self.usuario.is_tecnico, True)

    def test_paciente_creation(self):
        self.assertEqual(self.paciente.nombre_usuario, "Lizbeth")
        self.assertEqual(self.paciente.is_activo, False)
        self.assertEqual(self.paciente.is_paciente, True)
    
    def test_usuario_comun_login(self):
        self.user.set_password('1234')
        self.user.save()
        response = self.client.login(username=self.usuario_comun.username_usuario, password='1234')
        self.assertEqual(response, True)
"""
