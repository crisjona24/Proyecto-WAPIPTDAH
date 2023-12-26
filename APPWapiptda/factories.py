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
    user = factory.SubFactory(UserFactory)

class PacienteFactory(factory.Factory):
    class Meta:
        model = Paciente
    nombre_usuario = "Lizbeth"
    apellido_usuario = "Arias"
    email_usuario = "lizbeth.arias@unl.edu.ec"
    username_usuario = "LizbethArias"
    celular = "0999999999"
    fecha_nacimiento = "1999-10-10"
    dni = "1105339756"
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

# Fábrica de Dominio
class DominioFactory(factory.Factory):
    class Meta:
        model = Dominio

    id = 1
    nombre = "Dominio 1"
    descripcion = "Descripcion Dominio 1"
    identificador_dominio = 121212
    fecha_registro_dominio = "2020-10-10"
    usuario = factory.SubFactory(UsuarioFactory)

# Fábrica de Contenido
class ContenidoFactory(factory.Factory):
    class Meta:
        model = Contenido

    id = 1
    nombre = "Contenido 1"
    identificador_contenido = 121212
    dominio_tipo = "Sensorial"
    fecha_registro_contenido = "2020-10-10"
    dominio = factory.SubFactory(DominioFactory)

# Fábrica de Contenido Individual
class ContenidoIndividualFactory(factory.Factory):
    class Meta:
        model = ContenidoIndividual

    id = 1
    descripcion_individual = "Descripcion Contenido Individual 1"
    identificador_individual = 232323
    fecha_registro_individual = "2020-10-10"
    nivel = "Hiperactividad"
    tipo_contenido = "seleccion_individual"
    respuesta = "Respuesta Contenido Individual 1"
    contenido = factory.SubFactory(ContenidoFactory)

# Fabrica de Resultado
class ResultadoFactory(factory.Factory):
    class Meta:
        model = Resultado

    id = 1
    respuesta = "Respuesta Resultado 1"
    tiempo_m = 10
    tiempo_s = 5
    observacion = "Observacion Resultado 1"
    fecha_registro_resultado = "2020-10-10"
    contenido_individual = factory.SubFactory(ContenidoIndividualFactory)
    paciente = factory.SubFactory(PacienteFactory)

# Fábrica de Reportes
class ReporteFactory(factory.Factory):
    class Meta:
        model = Reporte

    id = 1
    titulo_reporte = "Reporte 1"
    descripcion_reporte = "Descripcion Reporte 1"
    fecha_registro_reporte = "2020-10-10"
    usuario_comun = factory.SubFactory(UsuarioComunFactory)
    resultado = factory.SubFactory(ResultadoFactory)

# Fábrica de Cursos
class CursoFactory(factory.Factory):
    class Meta:
        model = Curso

    id = 1
    nombre_curso = "Curso 1"
    descripcion_curso = "Descripcion Curso 1"
    identificador_curso = 454578
    fecha_registro_curso = "2020-10-10"
    usuario_comun = factory.SubFactory(UsuarioComunFactory)

# Fábrica de Registro de inscripción
class RegistroFactory(factory.Factory):
    class Meta:
        model = DetalleInscripcionCurso

    id = 1
    fecha_inscripcion = "2020-10-10"
    curso = factory.SubFactory(CursoFactory)
    paciente = factory.SubFactory(PacienteFactory)