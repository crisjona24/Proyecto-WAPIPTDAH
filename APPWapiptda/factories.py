import factory
from .models import *
from django.contrib.auth.models import User

class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = "JuanPerez"
    password = "1234"


class UsuarioComunFactory(factory.Factory):
    class Meta:
        model = UsuarioComun
    id = 1
    nombre_usuario = "Maria"
    apellido_usuario = "Arias"
    email_usuario = "maria.arias@unl.edu.ec"
    username_usuario = "MariaArias"
    celular = "0999999999"
    fecha_nacimiento = "1999-10-10"
    dni = "1234567890"
    fecha_registro_usuario = "2020-10-10"
    genero = "Femenino"
    area_estudio = "Ingenieria"
    user = factory.SubFactory(UserFactory)


class UsuarioFactory(factory.Factory):
    class Meta:
        model = Usuario

    nombre_usuario = "Juan"
    apellido_usuario = "Perez"
    email_usuario = "Juan.Perez@unl.edu.ec"
    username_usuario = "JuanPerez"
    celular = "0999999999"
    fecha_nacimiento = "1999-10-10"
    dni = "1234567890"
    fecha_registro_usuario = "2020-10-10"


class PacienteFactory(factory.Factory):
    class Meta:
        model = Paciente
    nombre_usuario = "Lizbeth"
    apellido_usuario = "Arias"
    email_usuario = "lizbeth.arias@unl.edu.ec"
    username_usuario = "LizbethArias"
    celular = "0999999999"
    fecha_nacimiento = "1999-10-10"
    dni = "1234567890"
    fecha_registro_usuario = "2020-10-10"
    contacto_emergencia = "0999999999"
    direccion = "Calle 1"


class GradoFactory(factory.Factory):
    class Meta:
        model = GradoTDAH
    
    id = 1
    nombre_nivel = "Primero"
    descripcion_grado = "Grado Primero"
    numero_categorias = 3
    grado_dificultad = "Alto"
    fecha_registro_grado = "2020-10-10"
    usuario_tecnico = factory.SubFactory(UsuarioFactory)