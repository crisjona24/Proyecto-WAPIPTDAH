from django.test import TestCase, Client
from APPWapiptda.models import *
from APPWapiptda.factories import *
from django.contrib.auth.models import User
from APPWapiptda.views import *
from EstudioyEntrenamiento.controlers import *
from django.urls import reverse

# API
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token

# Test de función para búsqueda de registros
class BuscarTestCase(TestCase):
    def setUp(self):
        self.cliente = Client()
        self.user = UserFactory.create() # User
        self.usuario = UsuarioFactory.create() # Usuario técnico
        self.user2 = User.objects.create_user(username='MariaArias',
                                              password='1234')
        self.usuario_comun = UsuarioComunFactory.create(user=self.user2) # Usuario común
        self.user3 = User.objects.create_user(username='LizbethArias',
                                              password='1234')
        self.paciente = PacienteFactory.create(user=self.user3) # Estudiante
        # Creamos objetos
        self.curso = CursoFactory.create() # Curso
        self.registro_incr = RegistroFactory.create() # Registro de inscripción

    def test_curso_creation(self):
        print("Verificar creación del curso y la inscripción")
        self.user2.set_password('1234')
        self.user2.save()
        response = self.cliente.login(username=self.usuario_comun.username_usuario,
                                      password='1234')
        self.user3.set_password('1234')
        self.user3.save()
        response_2 = self.cliente.login(username=self.paciente.username_usuario, 
                                        password='1234')
        self.assertEqual(response, True)
        self.assertEqual(response_2, True)
        self.assertEqual(self.usuario_comun.nombre_usuario, "Maria")
        self.assertEqual(self.usuario_comun.is_comun, True)
        # Verificar curso creado por un usuario comun
        self.assertEqual(
            self.curso.usuario_comun.username_usuario, "MariaArias")
        self.assertEqual(self.curso.usuario_comun.is_comun, True)
        # Verificar la inscripción del estudiante
        self.assertEqual(self.registro_incr.curso.nombre_curso, "Curso 1")
        self.assertEqual(self.registro_incr.paciente.username_usuario, "LizbethArias")

# Búsqueda de estudiante por cédula
class EstudianteCedulaListViewTest(TestCase):
    def setUp(self):
        self.cliente = Client()
        self.user = UserFactory.create() # User
        self.usuario = UsuarioFactory.create() # Usuario técnico
        self.user2 = User.objects.create_user(username='MariaArias',
                                              password='1234')
        self.usuario_comun = UsuarioComunFactory.create(user=self.user2) # Usuario común
        self.user3 = User.objects.create_user(username='LizbethArias',
                                              password='1234')
        self.paciente = PacienteFactory.create(user=self.user3) # Estudiante
        # Creamos objetos
        self.curso = CursoFactory.create() # Curso
        self.registro_incr = RegistroFactory.create() # Registro de inscripción

    def test_estudiante_cedula_list_view(self):
        print("Verificar búsqueda de estudiante por cédula")
        # Configurar el objeto de fábrica de solicitudes
        factory = APIRequestFactory()
        # Crear un objeto Request simulado con el encabezado de autorización
        token = '..--s9OjbWbd1pWjr6lA'
        request = factory.get(reverse('registro-estudiante', kwargs={'cedula': '1105339756', 'slug': 'curso-1-descripcion-curso-1'}), 
                              HTTP_AUTHORIZATION=f'Bearer {token}')
        # Asignar el usuario al objeto request (simula la autenticación)
        request.user = self.user2
        # Llamar a la vista con el objeto request simulado
        response = EstudianteCedulaListView.as_view()(request, cedula='1105339756', slug='curso-1-descripcion-curso-1')
        # Verificar el código de estado y la respuesta esperada
        self.assertEqual(response.status_code, 200) 
        # También puedes verificar que el método get_queryset está devolviendo los resultados esperados directamente
        queryset = EstudianteCedulaListView().get_queryset()
        self.assertIn(self.paciente, queryset)