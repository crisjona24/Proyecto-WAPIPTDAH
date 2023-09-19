import random
from django.db import IntegrityError
from .models import *
from .serializer import *
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, generics
from django.contrib.auth import authenticate, login, logout
import re
from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
import json
import cloudinary
import cloudinary.uploader
import cloudinary.api
# from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken, Token, UntypedToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.conf import settings
from django.core.mail import send_mail

### PAGINACION ###
from rest_framework.pagination import PageNumberPagination

class Paginacion(PageNumberPagination):
    page_size = 8

class Paginacion2(PageNumberPagination):
    page_size = 6

# Create your views here.

# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class UsuarioView(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class PacienteView(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ComunView(viewsets.ModelViewSet):
    queryset = UsuarioComun.objects.all()
    serializer_class = ComunSerializer

# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class GradoTDAHView(viewsets.ModelViewSet):
    queryset = GradoTDAH.objects.all()
    serializer_class = GraditoTDAHSerializer

# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class DominioView(viewsets.ModelViewSet):
    queryset = Dominio.objects.all().order_by('identificador_dominio')
    serializer_class = DominioSerializer
    pagination_class = Paginacion2

# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ContenidoView(viewsets.ModelViewSet):
    queryset = Contenido.objects.all().order_by('identificador_contenido')
    serializer_class = ContenidoSerializer
    pagination_class = Paginacion2

# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ContenidoIndividualView(viewsets.ModelViewSet):
    queryset = ContenidoIndividual.objects.all().order_by('-id')
    serializer_class = ContenidIndividualSerializer
    pagination_class = Paginacion2

# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ResultadoView(viewsets.ModelViewSet):
    queryset = Resultado.objects.all()
    serializer_class = ResultadoSerializer
    pagination_class = Paginacion

# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ResultadoViewOnly(viewsets.ModelViewSet):
    queryset = Resultado.objects.all()
    serializer_class = ResultadoSerializerOnly

# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CursoView(viewsets.ModelViewSet):
    queryset = Curso.objects.all().order_by('id')
    pagination_class = Paginacion
    serializer_class = CursoSerializer

# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class DetalleInscripcionCursoView(viewsets.ModelViewSet):
    queryset = DetalleInscripcionCurso.objects.all()
    serializer_class = DetalleInscripcionCursoSerializer

# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class PeticionView(viewsets.ModelViewSet):
    queryset = Peticion.objects.all()
    serializer_class = PeticionSerializer

# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class DetallePeticionView(viewsets.ModelViewSet):
    queryset = DetallePeticion.objects.all()
    serializer_class = DetallePeticionSerializer


# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class SalaView(viewsets.ModelViewSet):
    queryset = Sala.objects.all().order_by('nombre_sala')
    pagination_class = Paginacion
    serializer_class = SalaSerializer


# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class DetalleSalaView(viewsets.ModelViewSet):
    queryset = DetalleSala.objects.all()
    serializer_class = DetalleSalaSerializer
    pagination_class = Paginacion

# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ReporteView(viewsets.ModelViewSet):
    queryset = Reporte.objects.all().order_by('titulo_reporte')
    serializer_class = ReporteSerializer
    pagination_class = Paginacion

# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ListaSoloDominiosView(viewsets.ModelViewSet):
    queryset = Dominio.objects.all()
    serializer_class = DominioSerializer
    
# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ListaSoloContenidosView(viewsets.ModelViewSet):
    queryset = Contenido.objects.all()
    serializer_class = ContenidoSerializer

""" List """

# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ContenidoListView(generics.ListAPIView):
    serializer_class = ContenidoSerializer
    pagination_class = Paginacion2
    def get_queryset(self):
        slug_dominio = self.kwargs['slug']
        contenidos = lista_cotenido_dominio(slug_dominio)
        return contenidos

def lista_cotenido_dominio(ob1):
    try:
        # Obtener el dominio con el slug
        dominio_ob = Dominio.objects.get(slug_dominio=ob1)
        # Obtener los contenidos de un dominio
        contenidos = Contenido.objects.filter(dominio=dominio_ob)
        return contenidos
    except Dominio.DoesNotExist:
        return []
    except Contenido.DoesNotExist:
        return []


# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ContenidoIndividualListView(generics.ListAPIView):
    serializer_class = ContenidIndividualSerializer
    pagination_class = Paginacion2
    def get_queryset(self):
        slug_contenido = self.kwargs['slug']
        contenidos = lista_actividades_contenido(slug_contenido)
        return contenidos

def lista_actividades_contenido(ob1):
    try:
        # Obtener el contenido con el slug
        contenido_ob = Contenido.objects.get(slug_contenido=ob1)
        # Obtener los contenidos de un dominio
        contenidosIndividuales = ContenidoIndividual.objects.filter(contenido=contenido_ob)
        return contenidosIndividuales
    except Contenido.DoesNotExist:
        return []
    except ContenidoIndividual.DoesNotExist:
        return []


# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CoInNombreListView(generics.ListAPIView):
    serializer_class = ContenidIndividualSerializer
    pagination_class = Paginacion2
    def get_queryset(self):
        slug_contenido = self.kwargs['slug']
        nombre_nivel = self.kwargs['nombre']
        contenidos = lista_actividades_nombreNi(slug_contenido, nombre_nivel)
        return contenidos

def lista_actividades_nombreNi(ob1, ob2):
    try:
        # Obtener el contenido con el slug
        contenido_ob = Contenido.objects.get(slug_contenido=ob1)
        # Obtener el nivel por el nombre
        nivel_ob = GradoTDAH.objects.get(nombre_nivel=ob2)
        # Obtener los contenidos de un dominio y el nombre de nivel
        contenidosIndividualesN = ContenidoIndividual.objects.filter(nivel=nivel_ob.nombre_nivel, contenido=contenido_ob)
        return contenidosIndividualesN
    except Contenido.DoesNotExist:
        return []
    except GradoTDAH.DoesNotExist:
        return []
    except ContenidoIndividual.DoesNotExist:
        return []


# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ListaReporteUsuarioComun(generics.ListAPIView):
    serializer_class = ReporteSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtenemos el id del usuario
        id_usuario = self.kwargs['id']
        reportes = reporte_de_usuario(id_usuario)
        return reportes

def reporte_de_usuario(id_usuario):
    try: 
        # Encontrar el usuario comun por el id
        usuario_ob = UsuarioComun.objects.get(id=id_usuario)
        # Encontrar los reportes del usuario comun
        reportes = Reporte.objects.filter(usuario_comun=usuario_ob).order_by('titulo_reporte')
        return reportes
    except UsuarioComun.DoesNotExist:
        return []
    except Reporte.DoesNotExist:
        return []


# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class PeticionListViewNo(generics.ListAPIView):
    serializer_class = PeticionSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        return Peticion.objects.filter(estado_revision=False)
    
# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class PeticionListViewSi(generics.ListAPIView):
    serializer_class = PeticionSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        return Peticion.objects.filter(estado_revision=True)

# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class PeticionUCListView(generics.ListAPIView):
    serializer_class = PeticionSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        return Peticion.objects.filter(usuario_comun=self.kwargs['id'], estado_revision=True)


# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class PacientesListView(generics.ListAPIView):
    serializer_class = PacienteSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Encontrar el id
        id_curso = self.kwargs['id']
        pacientes = pacientes_list(id_curso)
        return pacientes

def pacientes_list(id_curso):
    try:
        # Filtrar registros de inscripción por curso
        inscripciones = DetalleInscripcionCurso.objects.filter(curso=id_curso, estado_detalle=True)
        # Obtiener solo los pacientes de esas inscripciones
        pacientes = [detalle.paciente for detalle in inscripciones]
        return pacientes
    except DetalleInscripcionCurso.DoesNotExist:
        return []

# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ResultadodePacienteListView(generics.ListAPIView):
    serializer_class = ResultadoSerializer
    # La busqueda es mediante el nombre y apellido del paciente
    def get_queryset(self):
        # Filtrar registros de inscripción por curso
        inscripciones = DetalleInscripcionCurso.objects.filter(curso=self.kwargs['id'], estado_detalle=True)
        # Obtiener solo los pacientes de esas inscripciones
        pacientes = [detalle.paciente for detalle in inscripciones]
        # Filtrar resultados por paciente
        resultados = Resultado.objects.filter(paciente__in=pacientes)
        return resultados

# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ResultadodePacienteListView2(generics.ListAPIView):
    serializer_class = ResultadoSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        nombre, apellido = self.kwargs['nombre'].split(' ', 1)
        if (nombre_paciente_exist(nombre , apellido)):
            # Filtrar registros de resultados por el nombre del paciente
            resultados = resultado_por_nombre(self.request, nombre, apellido)
            return resultados
        else:
            return []
        

def nombre_paciente_exist(nombre, apellido):
    # Verifica si el nombre del paciente ya existe
    try:
        if Paciente.objects.filter(nombre_usuario__iexact=nombre, apellido_usuario__iexact=apellido).exists():
            return True
    except Paciente.DoesNotExist:
        return False
    return False

def resultado_por_nombre(request, nombre, apellido):
    try:
        # Decodifica el token para obtener el usuario
        token = request.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        # Encontrar al usuario relacionado al user
        if is_comun(user):
            # Obtener el usuario comun
            usuario__ob = UsuarioComun.objects.get(user=user)
            # Obtener el paciente por nombre y apellido ignorando mayusculas y minusculas
            paciente__ob = Paciente.objects.get(nombre_usuario__icontains=nombre, apellido_usuario__icontains=apellido)
            # Obtener los cursos creados por el usuario comun
            cursos = Curso.objects.filter(usuario_comun=usuario__ob)
            # Obtener los cursos a los que está inscrito el paciente
            inscripciones = DetalleInscripcionCurso.objects.filter(paciente=paciente__ob, curso__in=cursos).exists()
            if inscripciones:
                # Obtener los resultados del paciente
                resultados = Resultado.objects.filter(paciente=paciente__ob).order_by('fecha_registro_resultado')
                return resultados
            else :
                return []
        else:
            if is_tecnico(user):
                # Obtener el paciente por nombre y apellido ignorando mayusculas y minusculas
                paciente__ob = Paciente.objects.get(nombre_usuario__icontains=nombre, apellido_usuario__icontains=apellido)
                # Obtener los resultados del paciente
                resultados = Resultado.objects.filter(paciente=paciente__ob).order_by('fecha_registro_resultado')
                return resultados
            else:
                return []
    except UsuarioComun.DoesNotExist:
        return []
    except Paciente.DoesNotExist:
        return []
    except Curso.DoesNotExist:
        return []
    except Resultado.DoesNotExist:
        return []
    


# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class SalasListView(generics.ListAPIView):
    serializer_class = SalaSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Encontrar el usuario comun por el id
        usuario_comun = UsuarioComun.objects.get(id=self.kwargs['id'])
        # Filtrar registro de sala asociada a un usuario comun
        salas = usuario_salas_list(usuario_comun)
        return salas

def usuario_salas_list(usuario_comun):
    try:
        # Encontrar al usuario relacionado al user
        if usuario_comun.is_comun:
            detalles_sala_usuario = DetalleSala.objects.filter(usuario_comun=usuario_comun)
            salas = Sala.objects.filter(detallesala__in=detalles_sala_usuario, sala_atendida=False).distinct()
            return salas
        else:
            return []
    except UsuarioComun.DoesNotExist:
        return []
    except DetalleSala.DoesNotExist:
        return []

# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class SalasAtendidasListView(generics.ListAPIView):
    serializer_class = SalaSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Encontrar el usuario comun por el id
        usuario_comun = UsuarioComun.objects.get(id=self.kwargs['id'])
        # Filtrar registro de sala asociada a un usuario comun
        salas = usuario_salas_list_a(usuario_comun)
        return salas

def usuario_salas_list_a(usuario_comun):
    try:
        # Encontrar al usuario relacionado al user
        if usuario_comun.is_comun:
            detalles_sala_usuario = DetalleSala.objects.filter(usuario_comun=usuario_comun)
            salas = Sala.objects.filter(detallesala__in=detalles_sala_usuario, sala_atendida=True).distinct()
            return salas
        else:
            return []
    except UsuarioComun.DoesNotExist:
        return []
    except DetalleSala.DoesNotExist:
        return []

# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CursosListView(generics.ListAPIView):
    serializer_class = CursoSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        cursos = usuario_cursos_list(self.request)
        return cursos

def usuario_cursos_list(request):
    try:
        # Decodifica el token para obtener el usuario
        token = request.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        # Encontrar al usuario relacionado al user
        if is_comun(user):
            usuario__ob = UsuarioComun.objects.get(user=user)
            # Verificar si el usuario existe
            if user and usuario__ob:
                # Verificar el tipo de usuario
                if usuario__ob.is_comun:
                    cursos = Curso.objects.filter(usuario_comun=usuario__ob).order_by('id')
                    print("Saque los cursos del usuario")
                    return cursos
            else:
                return []
        else:
            return []
    except UsuarioComun.DoesNotExist:
        return []

# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class SalasPacienteListView(generics.ListAPIView):
    serializer_class = SalaSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Encontrar el paciente por el id
        paciente = Paciente.objects.get(id=self.kwargs['id'])
        # Filtrar registro de sala asociada a un paciente
        salas = Sala.objects.filter(paciente=paciente, sala_atendida=False, estado_sala=True)
        return salas

# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class BusquedaSalasListView(generics.ListAPIView):
    serializer_class = SalaSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Encontrar el nombre de sala de la url
        nombre_sala = self.kwargs['nombre']
        if nombre_sala_exist(nombre_sala):
            # Filtrar registro de sala asociada al nombre de sala
            salas = Sala.objects.filter(nombre_sala__icontains=nombre_sala)
            return salas
        else:
            return []

def nombre_sala_exist(nombre):
    # Verifica si el nombre de la sala ya existe
    try:
        Sala.objects.filter(nombre_sala__iexact=nombre).exists()
        return True
    except Sala.DoesNotExist:
        return False



# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class BusquedaContenidoListView(generics.ListAPIView):
    serializer_class = ContenidoSerializer
    pagination_class = Paginacion2
    def get_queryset(self):
        # Encontrar el nombre de sala de la url
        nombre_contenido = self.kwargs['nombre']
        slug_dominio = self.kwargs['slug']
        if nombre_contenido_exist(nombre_contenido):
            # Filtrar registro de sala asociada al nombre de sala
            contenidos = Contenido.objects.filter(nombre__icontains=nombre_contenido, dominio__slug_dominio=slug_dominio)
            return contenidos
        else:
            return []

def nombre_contenido_exist(nombre):
    # Verifica si el nombre del contenido ya existe
    try:
        if Contenido.objects.filter(nombre__iexact=nombre).exists():
            return True
    except Contenido.DoesNotExist:
        return False
    return False


# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class BusquedaCursoListView(generics.ListAPIView):
    serializer_class = CursoSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Encontrar el nombre de sala de la url
        nombre_curso = self.kwargs['nombre']
        if nombre_curso_exist(nombre_curso):
            # Filtrar registro de sala asociada al nombre de sala
            cursos = Curso.objects.filter(nombre_curso__icontains=nombre_curso)
            return cursos
        else:
            return []

def nombre_curso_exist(nombre):
    # Verifica si el nombre del curso ya existe
    try:
        if Curso.objects.filter(nombre_curso__iexact=nombre).exists():
            return True
    except Curso.DoesNotExist:
        return False
    return False

# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class BusquedaPacienteCursoListView(generics.ListAPIView):
    serializer_class = PacienteSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Encontrar el nombre del paciente de la url
        nombre, apellido = self.kwargs['nombre'].split(' ', 1)
        slug_cur = self.kwargs['slug']
        if (paciente_exist_curso(nombre, apellido, slug_cur)):
            # obtener paciente
            paciente = obtener_paciente(nombre, apellido)
            return paciente
        else:
            return []
        
def paciente_exist_curso(ob1, ob2, ob3):
    # Verifica si el nombre del paciente ya existe en un curso
    try:
        # obtener el registro de curso del detalle de inscripcion
        curso = Curso.objects.get(slug_curso=ob3)
        # obtener el paciente por nombre y apellido ignorando mayusculas y minusculas
        paciente = Paciente.objects.get(nombre_usuario__iexact=ob1, apellido_usuario__iexact=ob2)
        # Verificar una inscripcion a ese curso del paciente
        if DetalleInscripcionCurso.objects.filter(paciente=paciente, curso=curso).exists():
            return True
    except DetalleInscripcionCurso.DoesNotExist:
        return False
    except Paciente.DoesNotExist:
        return False
    except Curso.DoesNotExist:
        return False
    return False


def obtener_paciente(ob1, ob2):
    # Verifica si el nombre del paciente ya existe en un curso
    try:
        # obtener el paciente por nombre y apellido ignorando mayusculas y minusculas
        paciente = Paciente.objects.filter(nombre_usuario__iexact=ob1, apellido_usuario__iexact=ob2).order_by('nombre_usuario')
        return paciente
    except Paciente.DoesNotExist:
        return []   


# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ResultadoListaUsuario(generics.ListAPIView):
    serializer_class = ResultadoSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtenemos el id del usuario
        id_usuario = self.kwargs['id']
        resultados = resultado_de_usuario(id_usuario)
        return resultados

def resultado_de_usuario(id_usuario):
    try: 
        # Encontrar el usuario comun por el id
        usuario_comun_especifico = UsuarioComun.objects.get(id=id_usuario)
        # Encontrar los cursos creados por ese UsuarioComun
        cursos = Curso.objects.filter(usuario_comun=usuario_comun_especifico)
        # Encontrar los pacientes inscritos en esos cursos
        pacientes_inscritos_curso = Paciente.objects.filter(detalleinscripcioncurso__curso__in=cursos).distinct()
        # Encotrar los resultados de esos pacientes
        resultados = Resultado.objects.filter(paciente__in=pacientes_inscritos_curso).order_by('-fecha_registro_resultado')
        return resultados
    except UsuarioComun.DoesNotExist:
        return []
    except Curso.DoesNotExist:
        return []
    except Paciente.DoesNotExist:
        return []
    except Resultado.DoesNotExist:
        return []

## METODOS VARIOS ###

def validar_clave(ob1):
    """
    Controlar si la contraseña cumple con las especificaciones de seguridad mínimas.
    - Al menos 8 caracteres.
    - Al menos una letra mayúscula.
    - Al menos una letra minúscula.
    - Al menos un número.
    - Al menos un símbolo.
    """
    if len(ob1) < 8:
        return False
    if not re.search(r"[A-Z]", ob1):
        return False
    if not re.search(r"[a-z]", ob1):
        return False
    if not re.search(r"[0-9]", ob1):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", ob1):
        return False
    return True

def generar_identificador_unico():
    """Genera un identificador único para Dominio."""
    identificador = str(random.randint(1000, 9999))
    while Dominio.objects.filter(identificador_dominio=identificador).exists():
        identificador = str(random.randint(1000, 9999))
    return identificador

def generar_identificador_contenido():
    """Genera un identificador único para Contenido."""
    identificador_c = str(random.randint(10000, 20000))
    while Contenido.objects.filter(identificador_contenido=identificador_c).exists():
        identificador_c = str(random.randint(10000, 20000))
    return identificador_c

def generar_identificador_individual():
    """Genera un identificador único para Contenido Individual."""
    identificador_i = str(random.randint(20001, 30000))
    while ContenidoIndividual.objects.filter(identificador_individual=identificador_i).exists():
        identificador_i = str(random.randint(20001, 30000))
    return identificador_i

def generar_identificador_curso():
    """Genera un identificador único para Curso."""
    identificador_c = str(random.randint(30001, 40000))
    while Curso.objects.filter(identificador_curso=identificador_c).exists():
        identificador_c = str(random.randint(30001, 40000))
    return identificador_c

def is_tecnico(user):
    """Verifica si el usuario es un técnico."""
    try:
        usuario__ob = Usuario.objects.get(user=user)
        if usuario__ob.is_tecnico:
            return True
        else:
            return False
    except Usuario.DoesNotExist:
        return False

def is_comun(user):
    """Verifica si el usuario es un usuario comun."""
    try:
        usuario__ob = UsuarioComun.objects.get(user=user)
        if usuario__ob.is_comun:
            return True
        else:
            return False
    except UsuarioComun.DoesNotExist:
        return False

def is_paciente(user):
    """Verifica si el usuario es un paciente."""
    try:
        usuario__ob = Paciente.objects.get(user=user)
        if usuario__ob.is_paciente:
            return True
        else:
            return False
    except Paciente.DoesNotExist:
        return False   
    

# METODO DE INICIO DE SESION DE USUARIO
@api_view(['POST'])
def api_login(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username=username, password=password)
            # Autenticar usuario
            if user is not None:
                if user.is_authenticated:
                    login(request, user)
                    """token, _ = Token.objects.get_or_create(user=user)
                    context = {
                        'success': True,
                        'token': token.key,
                    }"""
                    refresh=RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    # Verificamos el tipo de usuario
                    if is_paciente(user):
                        context = {
                            'success': True,
                            'tipo': 'paciente',
                            'token': access_token,
                        }
                        # Response({'token': token.key})
                        return JsonResponse(context)
                    elif is_tecnico(user):
                        context = {
                            'success': True,
                            'tipo': 'tecnico',
                            'token': access_token,
                        }
                        return JsonResponse(context)
                    elif is_comun(user):
                        context = {
                            'success': True,
                            'tipo': 'comun',
                            'token': access_token,
                        }
                        return JsonResponse(context)
                else:
                    context = {
                        'error': 'Usuario o contraseña incorrectos',
                    }
                    return JsonResponse(context)
            else:
                context = {
                    'error': 'Usuario o contraseña incorrectos',
                }
                return JsonResponse(context, status=401)
        else:
            return JsonResponse({'error': 'Ups! Algo salió mal'}, status=405)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# METODO DE CERRAR SESION DE USUARIO
@api_view(['POST'])
def api_logout(request):
    logout(request)
    return JsonResponse({'success': True})

## VERIFICAR USUARIO ###
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def verificar_usuario(request):
    if request.user.is_authenticated:
        # Decodifica el token para obtener el usuario
        token = request.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        try:
            # Encontrar al usuario relacionado al user
            usuario__ob = Usuario.objects.get(user=user)
            # Verificar si el usuario existe
            if user and usuario__ob:
                # Verificar el tipo de usuario
                if usuario__ob.is_tecnico:
                    context = {
                        'success': True,
                        'tipo': 'tecnico',
                        'identificador': usuario__ob.id,
                    }
                    return JsonResponse(context)
            else:
                return JsonResponse({'error': 'El usuario no existe'}, status=401)
        except Usuario.DoesNotExist:
            try:
                # Encontrar al usuario relacionado al user
                paciente__ob = Paciente.objects.get(user=user)
                # Verificar si el usuario existe
                if user and paciente__ob:
                    # Verificar el tipo de usuario
                    if paciente__ob.is_paciente:
                        context = {
                            'success': True,
                            'tipo': 'paciente',
                            'identificador': paciente__ob.id,
                        }
                        return JsonResponse(context)
                else:
                    return JsonResponse({'error': 'El usuario no existe'}, status=401)
            except Paciente.DoesNotExist:
                try:
                    # Encontrar al usuario relacionado al user
                    comun__ob = UsuarioComun.objects.get(user=user)
                    # Verificar si el usuario existe
                    if user and comun__ob:
                        # Verificar el tipo de usuario
                        if comun__ob.is_comun:
                            context = {
                                'success': True,
                                'tipo': 'comun',
                                'identificador': comun__ob.id,
                            }
                            return JsonResponse(context)
                    else:
                        return JsonResponse({'error': 'El usuario no existe'}, status=401)
                except UsuarioComun.DoesNotExist:
                    return JsonResponse({'error': 'El usuario no existe'}, status=401)
    else:
        return JsonResponse({'error': 'El usuario no esta autenticado'}, status=401)
        


## VERIFICAR NIVEL ###
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def verificar_nivel(request, slug):
    if request.user.is_authenticated:
        try:
            # Decodifica el token
            token = request.headers.get('Authorization').split(" ")[1]
            user = get_user_from_token_jwt(token)
            #user = get_user_from_token(token)
            if is_tecnico(user):
                if request.method == 'GET':
                    # Obtenemos el objeto grado tdah
                    grado__ob = GradoTDAH.objects.get(slug_grado=slug)
                    context = {
                        'success': True,
                        'identificador': grado__ob.id,
                        'slug': slug
                    }
                    return JsonResponse(context)
                else:
                    context = {'error': 'Error al mostrar datos de nivel'}
                    return JsonResponse(context)
            else:
                context = {'errorSalida': 'El usuario no esta autenticado'}
                return JsonResponse(context, status=401)
        except Exception as e:
            context = {'errorSalida': 'El usuario no esta autenticado'}
            return JsonResponse(context, status=500)
    else:
        return JsonResponse({'error': 'El usuario no esta autenticado'}, status=401)


## VERIFICAR DOMINIO ###
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def verificar_dominio(request, slug):
    if request.user.is_authenticated:
        try:
            # Decodifica el token
            token = request.headers.get('Authorization').split(" ")[1]
            user = get_user_from_token_jwt(token)
            #user = get_user_from_token(token)
            if user and token:
                if request.method == 'GET':
                    # Obtenemos el objeto dominio
                    dominio__ob = Dominio.objects.get(slug_dominio=slug)
                    context = {
                        'success': True,
                        'identificador': dominio__ob.id,
                        'slug': slug
                    }
                    return JsonResponse(context)
                else:
                    context = {'error': 'Error al mostrar datos de dominio'}
                    return JsonResponse(context)
            else:
                context = {'errorSalida': 'El usuario no esta autenticado'}
                return JsonResponse(context, status=401)
        except Exception as e:
            context = {'errorSalida': 'El usuario no esta autenticado'}
            return JsonResponse(context, status=500)
    else:
        return JsonResponse({'error': 'El usuario no esta autenticado'}, status=401)


## VERIFICAR CONTENIDO ###
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def verificar_contenido(request, slug):
    if request.user.is_authenticated:
        try:
            # Verificar existencia de token
            token = request.headers.get('Authorization').split(" ")[1]
            user = get_user_from_token_jwt(token)
            #user = get_user_from_token(token)
            if user and token:
                # Encontrar el contenido en base al slug
                contenido__ob = Contenido.objects.get(slug_contenido=slug)
                # Verificar si el dominio existe
                if contenido__ob:
                    context = {
                        'success': True,
                        'identificador': contenido__ob.id,
                        'slug': slug
                    }
                    return JsonResponse(context)
                else:
                    context = {'error': 'Error al mostrar datos de contenido'}
                    return JsonResponse(context)
            else:
                context = {'errorSalida': 'El usuario no esta autenticado'}
                return JsonResponse(context, status=401)
        except Exception as e:
            context = {'errorSalida': 'El usuario no esta autenticado'}
            return JsonResponse(context, status=500)
    else:
        return JsonResponse({'error': 'El usuario no esta autenticado'}, status=401)


## VERIFICAR CONTENIDO INDIVIDUAL ###
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def verificar_contenido_individual(request, slug):
    if request.user.is_authenticated:
        try:
            # Verificar existencia de token
            token = request.headers.get('Authorization').split(" ")[1]
            user = get_user_from_token_jwt(token)
            #user = get_user_from_token(token)
            if user and token:
                # Encontrar el contenido en base al slug
                contenido__ob = ContenidoIndividual.objects.get(slug_contenido_individual=slug)
                # Verificar si el dominio existe
                if contenido__ob:
                    context = {
                        'success': True,
                        'identificador': contenido__ob.id,
                        'slug': slug
                    }
                    return JsonResponse(context)
                else:
                    context = {'error': 'Error al mostrar datos de contenido individual'}
                    return JsonResponse(context)
            else:
                context = {'errorSalida': 'El usuario no esta autenticado'}
                return JsonResponse(context, status=401)
        except Exception as e:
            context = {'errorSalida': 'El usuario no esta autenticado'}
            return JsonResponse(context, status=500)
    else:
        return JsonResponse({'error': 'El usuario no esta autenticado'}, status=401)


## VERIFICAR CURSO ###
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def verificar_curso(request, slug):
    if request.user.is_authenticated:
        try:
            # Verificar existencia de token
            token = request.headers.get('Authorization').split(" ")[1]
            user = get_user_from_token_jwt(token)
            #user = get_user_from_token(token)
            if is_comun(user):
                # Encontrar el contenido en base al slug
                curso__ob = Curso.objects.get(slug_curso=slug)
                # Verificar si el dominio existe
                if curso__ob:
                    context = {
                        'success': True,
                        'identificador': curso__ob.id,
                        'slug': slug
                    }
                    return JsonResponse(context)
                else:
                    context = {'error': 'Error al mostrar datos de curso'}
                    return JsonResponse(context)
            else:
                context = {'errorSalida': 'El usuario no esta autenticado'}
                return JsonResponse(context, status=401)
        except Exception as e:
            context = {'errorSalida': 'El usuario no esta autenticado'}
            return JsonResponse(context, status=500)
    else:
        return JsonResponse({'error': 'El usuario no esta autenticado'}, status=401)


## VERIFICAR PETICION ###
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def verificar_peticion(request, slug):
    if request.user.is_authenticated:
        try:
            # Verificar existencia de token
            token = request.headers.get('Authorization').split(" ")[1]
            user = get_user_from_token_jwt(token)
            #user = get_user_from_token(token)
            if user and token:
                # Encontrar el contenido en base al slug
                peticion__ob = Peticion.objects.get(slug_peticion=slug)
                # Verificar si el dominio existe
                if peticion__ob:
                    context = {
                        'identificador': peticion__ob.id,
                        'slug': slug
                    }
                    return JsonResponse(context)
                else:
                    context = {'error': 'Error al mostrar datos de peticion'}
                    return JsonResponse(context)
            else:
                context = {'errorSalida': 'El usuario no esta autenticado'}
                return JsonResponse(context, status=401)
        except Exception as e:
            context = {'errorSalida': 'El usuario no esta autenticado'}
            return JsonResponse(context, status=500)
    else:
        return JsonResponse({'error': 'El usuario no esta autenticado'}, status=401)

## VERIFICAR CONTENIDO ###
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def verificar_resultado(request, slug):
    try:
        # Verificar existencia de token
        token = request.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        #user = get_user_from_token(token)
        if user and token:
            # Encontrar el resultado en base al slug
            resultado__ob = Resultado.objects.get(slug_resultado=slug)
            # Verificar si el dominio existe
            if resultado__ob:
                context = {
                    'identificador': resultado__ob.id,
                    'slug': slug
                }
                return JsonResponse(context)
            else:
                context = {'error': 'Error al mostrar datos de resultado'}
                return JsonResponse(context)
        else:
            context = {'errorSalida': 'El usuario no esta autenticado'}
            return JsonResponse(context, status=401)
    except Exception as e:
        context = {'errorSalida': 'El usuario no esta autenticado'}
        return JsonResponse(context, status=500)



## VERIFICAR SALA ###
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def verificar_sala(request, slug):
    try:
        # Verificar existencia de token
        token = request.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        #user = get_user_from_token(token)
        if user and token:
            # Encontrar el resultado en base al slug
            sala__ob = Sala.objects.get(slug_sala=slug)
            # Verificar si el dominio existe
            if sala__ob:
                context = {
                    'identificador': sala__ob.id,
                    'slug': slug
                }
                return JsonResponse(context)
            else:
                context = {'error': 'Error al mostrar datos de sala'}
                return JsonResponse(context)
        else:
            context = {'errorSalida': 'El usuario no esta autenticado'}
            return JsonResponse(context, status=401)
    except Exception as e:
        context = {'errorSalida': 'El usuario no esta autenticado'}
        return JsonResponse(context, status=500)


## VERIFICAR REPORTE ###
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def verificar_reporte(request, slug):
    try:
        # Verificar existencia de token
        token = request.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        #user = get_user_from_token(token)
        if user and token:
            # Encontrar el resultado en base al slug
            reporte_ob = Reporte.objects.get(slug_reporte=slug)
            # Verificar si el dominio existe
            if reporte_ob:
                context = {
                    'identificador': reporte_ob.id,
                    'slug': slug
                }
                return JsonResponse(context)
            else:
                context = {'error': 'Error al mostrar datos de reporte'}
                return JsonResponse(context)
        else:
            context = {'errorSalida': 'El usuario no esta autenticado'}
            return JsonResponse(context, status=401)
    except Exception as e:
        context = {'errorSalida': 'El usuario no esta autenticado'}
        return JsonResponse(context, status=500)


## DATOS USUARIO ###
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def datos_usuario(request):
    if request.user.is_authenticated:
        # Decodifica el token para obtener el usuario
        token = request.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        #user = get_user_from_token(token)
        try:
            # Encontrar al usuario relacionado al user
            usuario__ob = Usuario.objects.get(user=user)
            # Verificar si el usuario existe
            if user and usuario__ob:
                # Verificar el tipo de usuario
                if usuario__ob.is_tecnico:
                    context = {
                        'success': True,
                        'tipo': 'tecnico',
                        'nombre': usuario__ob.nombre_usuario,
                        'apellido': usuario__ob.apellido_usuario,
                        'email': usuario__ob.email_usuario,
                        'username': usuario__ob.username_usuario,
                        'edad': usuario__ob.edad,
                        'identificador': user.id,
                    }
                    return JsonResponse(context)
            else:
                return JsonResponse({'success': False})
        except Usuario.DoesNotExist:
            try:
                # Encontrar al usuario relacionado al user
                paciente__ob = Paciente.objects.get(user=user)
                # Verificar si el usuario existe
                if user and paciente__ob:
                    # Verificar el tipo de usuario
                    if paciente__ob.is_paciente:
                        context = {
                            'success': True,
                            'tipo': 'paciente',
                            'nombre': paciente__ob.nombre_usuario,
                            'apellido': paciente__ob.apellido_usuario,
                            'email': paciente__ob.email_usuario,
                            'celular': paciente__ob.celular,
                            'contacto_emergencia': paciente__ob.contacto_emergencia,
                            'fecha_nacimiento': paciente__ob.fecha_nacimiento,
                            'edad': paciente__ob.edad,
                            'identificador': user.id,
                        }
                        return JsonResponse(context)
                else:
                    return JsonResponse({'success': False})
            except Paciente.DoesNotExist:
                try:
                    # Encontrar al usuario relacionado al user
                    comun__ob = UsuarioComun.objects.get(user=user)
                    # Verificar si el usuario existe
                    if user and comun__ob:
                        # Verificar el tipo de usuario
                        if comun__ob.is_comun:
                            context = {
                                'success': True,
                                'tipo': 'comun',
                                'nombre': comun__ob.nombre_usuario,
                                'apellido': comun__ob.apellido_usuario,
                                'email': comun__ob.email_usuario,
                                'celular': comun__ob.celular,
                                'fecha_nacimiento': comun__ob.fecha_nacimiento,
                                'genero': comun__ob.genero,
                                'area_estudio': comun__ob.area_estudio,
                                'edad': comun__ob.edad,
                                'identificador': user.id,
                            }
                            return JsonResponse(context)
                    else:
                        return JsonResponse({'success': False})
                except UsuarioComun.DoesNotExist:
                    return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': False})

### OBTENER EL USUARIO DEL TOKEN ###
def get_user_from_token(key):
    try:
        token = Token.objects.get(key=key)
        return token.user
    except Token.DoesNotExist:
        return None

def get_user_from_token_jwt(key):
    try:
        # Validar el token y obtener el payload
        UntypedToken(key)
        
        # Obtener el user de JWTAuthentication
        jwt_auth = JWTAuthentication()
        validated_token = jwt_auth.get_validated_token(key)
        user = jwt_auth.get_user(validated_token)
        return user
    except TokenError:
        raise InvalidToken("Error al decodificar el token.")


#### METODOS SIN VALIDACION DE TOKEN ####
def existe__registro(ob1, ob2):
    try:
        if Paciente.objects.filter(nombre_usuario__iexact=ob1, apellido_usuario__iexact=ob2).exists():
            return True
        elif UsuarioComun.objects.filter(nombre_usuario__iexact=ob1, apellido_usuario__iexact=ob2).exists():
            return True
        elif Usuario.objects.filter(nombre_usuario__iexact=ob1, apellido_usuario__iexact=ob2).exists():
            return True
    except Paciente.DoesNotExist:
        return False
    except UsuarioComun.DoesNotExist:
        return False
    except Usuario.DoesNotExist:
        return False
    return False

def username_exist(ob1):
    try:
        if Paciente.objects.filter(username_usuario__iexact=ob1).exists():
            return True
        elif UsuarioComun.objects.filter(username_usuario__iexact=ob1).exists():
            return True
        elif Usuario.objects.filter(username_usuario__iexact=ob1).exists():
            return True
    except Paciente.DoesNotExist:
        return False
    except UsuarioComun.DoesNotExist:
        return False
    except Usuario.DoesNotExist:
        return False
    return False

# METODO DE REGISTRO DE USUARIO
@api_view(['POST'])
def api_user_register(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            first_name_ = data.get('nombre_usuario')
            last_name_ = data.get('apellido_usuario')
            email_ = data.get('email_usuario')
            username_ = data.get('username_usuario')
            password_ = data.get('password_usuario')
            celular_ = data.get('celular')
            fecha_ = data.get('fecha_nacimiento')
            if validar_clave(password_) == False:
                return JsonResponse({'clave': 'Clave sin requisitos mínimos'})
            # Verificar si el usuario ya existe
            if existe__registro(first_name_, last_name_):
                return JsonResponse({'error': 'El usuario ya existe'})
            else:
                if username_exist(username_):
                    return JsonResponse({'error': 'El nombre de usuario ya existe'})
                else:
                    # Creamos el usuario
                    user = User.objects.create(
                        first_name=first_name_,
                        last_name=last_name_,
                        password=make_password(password_),
                        username=username_,
                        email=email_
                    )
                    # Añadimos a usuario
                    user.save()
                    crear_usuario_normal(first_name_, last_name_, email_, username_, fecha_, celular_, user)
                    return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Método no permitido'})
    except Exception as e:
        return JsonResponse({'error': 'Error al crear el usuario'})

def crear_usuario_normal(ob1, ob2, ob3, ob4, ob5, ob6, ob7):
    usuario__model = Usuario.objects.create(
        nombre_usuario=ob1,
        apellido_usuario=ob2,
        email_usuario=ob3,
        username_usuario=ob4,
        fecha_nacimiento=ob5,
        celular=ob6,
        user=ob7
    )
    # Añadimos a usuario
    usuario__model.save()

# METODO DE REGISTRO DE PACIENTE
@api_view(['POST'])
def api_paciente_register(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            first_name_ = data.get('nombre_usuario')
            last_name_ = data.get('apellido_usuario')
            email_ = data.get('email_usuario')
            username_ = data.get('username_usuario')
            password_ = data.get('password_usuario')
            celular_ = data.get('celular')
            fecha_ = data.get('fecha_nacimiento')
            contacto_emergencia_ = data.get('contacto_emergencia')
            direccion_ = data.get('direccion')
            if validar_clave(password_) == False:
                return JsonResponse({'clave': 'Clave sin requisitos mínimos'})
            # Verificar si el usuario ya existe
            if existe__registro(first_name_, last_name_):
                return JsonResponse({'error': 'El usuario ya existe'})
            else:
                if username_exist(username_):
                    return JsonResponse({'error': 'El nombre de usuario ya existe'})
                else:
                    # Creamos el usuario
                    user_new = User.objects.create(
                        first_name=first_name_,
                        last_name=last_name_,
                        password=make_password(password_),
                        username=username_,
                        email=email_
                    )
                    # Añadimos a usuario
                    user_new.save()
                    crear_paciente_normal(first_name_, last_name_, email_, username_, celular_, contacto_emergencia_, fecha_, direccion_, user_new)
                    return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Método no permitido'})
    except Exception as e:
        return JsonResponse({'error': 'Error al crear el usuario'})

def crear_paciente_normal(ob1, ob2, ob3, ob4, ob5, ob6, ob7, ob8, ob9):
    usuario__model = Paciente.objects.create(
        nombre_usuario=ob1,
        apellido_usuario=ob2,
        email_usuario=ob3,
        username_usuario=ob4,
        celular=ob5,
        contacto_emergencia=ob6,
        fecha_nacimiento=ob7,
        direccion=ob8,
        user=ob9
    )
    # Añadimos a usuario
    usuario__model.save()

# METODO DE REGISTRO DE USUARIO COMUN
@api_view(['POST'])
def api_comun_register(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            first_name_ = data.get('nombre_usuario')
            last_name_ = data.get('apellido_usuario')
            email_ = data.get('email_usuario')
            username_ = data.get('username_usuario')
            password_ = data.get('password_usuario')
            celular_ = data.get('celular')
            fecha_ = data.get('fecha_nacimiento')
            genero_ = data.get('genero')
            area_ = data.get('area_estudio')
            if validar_clave(password_) == False:
                return JsonResponse({'clave': 'Clave sin requisitos mínimos'})
            # Verificar si el usuario ya existe
            if existe__registro(first_name_, last_name_):
                return JsonResponse({'error': 'El usuario ya existe'})
            else:
                if username_exist(username_):
                    return JsonResponse({'error': 'El nombre de usuario ya existe'})
                else:
                    # Creamos el usuario
                    user = User.objects.create(
                        first_name=first_name_,
                        last_name=last_name_,
                        password=make_password(password_),
                        username=username_,
                        email=email_
                    )
                    # Añadimos a usuario
                    user.save()
                    crear_comun_normal(first_name_, last_name_, email_, username_, celular_, fecha_, genero_, area_, user)
                    return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Método no permitido'})
    except Exception as e:
        return JsonResponse({'error': 'Error al crear el usuario'})

def crear_comun_normal(ob1, ob2, ob3, ob4, ob5, ob6, ob7, ob8, ob9):
    usuario__model = UsuarioComun.objects.create(
        nombre_usuario=ob1,
        apellido_usuario=ob2,
        email_usuario=ob3,
        username_usuario=ob4,
        celular=ob5,
        fecha_nacimiento=ob6,
        genero=ob7,
        area_estudio=ob8,
        user=ob9
    )
    # Añadimos a usuario
    usuario__model.save()

#### FIN DE METODOS SIN VALIDACION DE TOKEN ####

#  METODO PARA REGISTRO DE GRADO TDAH
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def api_nivel_register(request):
    if request.user.is_authenticated:
        try:
            # Decodifica el token para obtener el usuario
            token = request.headers.get('Authorization').split(" ")[1]
            user = get_user_from_token_jwt(token)
            #user = get_user_from_token(token)
            # Validamos si el usuario es tecnico
            if is_tecnico(user):
                # Encontrar al usuario relacionado al user
                usuario__ob = Usuario.objects.get(user=user)
                # Verificar si el usuario existe
                if request.method == 'POST' and user:
                    data = json.loads(request.body)
                    nombre_nivel_ = data.get('nombre')
                    descripcion_grado_ = data.get('descripcion')
                    numero_categorias_ = data.get('numero_categorias')
                    grado_dificultad_ = data.get('grado_dificultad')
                    cont = numero_de_niveles()
                    if cont < 2:
                        # Verificar si el nombre del nivel ya existe
                        if nombre_nivel_exist(nombre_nivel_):
                            return JsonResponse({'error': 'El nombre del nivel ya existe'})
                        else:
                            # Creamos el grado
                            if guardar_nivel(nombre_nivel_, descripcion_grado_, numero_categorias_, grado_dificultad_, usuario__ob):
                                return JsonResponse({'success': True})
                            else:
                                return JsonResponse({'error': 'Error al guardar el nivel'})
                    else:
                        return JsonResponse({'error': 'Solo se permite 2 niveles'})
                else:
                    return JsonResponse({'error': 'No esta permitido'})
            else:
                return JsonResponse({'error': 'El usuario no esta autenticado'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'El usuario no esta autenticado'})

def guardar_nivel(ob1, ob2, ob3, ob4, ob5):
    try:
        grado = GradoTDAH.objects.create(
            nombre_nivel=ob1,
            descripcion_grado=ob2,
            numero_categorias=ob3,
            grado_dificultad=ob4,
            usuario_tecnico=ob5
        )
        # Añadimos a contenido
        grado.save()
        return True
    except Exception as e:
        return False

def nombre_nivel_exist(ob1):
    try:
        if GradoTDAH.objects.filter(nombre_nivel__iexact=ob1).exists():
            return True
    except GradoTDAH.DoesNotExist:
        return False
    return False

def numero_de_niveles():
    try:
        return GradoTDAH.objects.all().count()
    except GradoTDAH.DoesNotExist:
        return 0
    
# METODO DE REGISTRO DE DOMINIO
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def api_dominio_register(request):
    if request.user.is_authenticated:
        try:
            # Decodifica el token para obtener el usuario
            token = request.headers.get('Authorization').split(" ")[1]
            user = get_user_from_token_jwt(token)
            #user = get_user_from_token(token)
            # Validamos si el usuario es tecnico
            if is_tecnico(user):
                # Encontrar al usuario relacionado al user
                usuario__ob = Usuario.objects.get(user=user)
                # Verificar si el usuario existe
                if request.method == 'POST' and user:
                    nombre_dominio_ = request.POST.get('nombre')
                    descripcion_ = request.POST.get('descripcion')
                    portada_ = request.FILES.get(
                        'portada_dominio')  # obtener archivo
                    # Verificar si el nombre del dominio ya existe
                    if nombre_dominio_exist(nombre_dominio_):
                        return JsonResponse({'error': 'El nombre del dominio ya existe'})
                    else:
                        # Calculamos el identificador
                        identificador_ = generar_identificador_unico()
                        # Creamos el contenido
                        if guardar_dominio(nombre_dominio_, identificador_, descripcion_, portada_, usuario__ob):
                            return JsonResponse({'success': True})
                        else:
                            return JsonResponse({'error': 'Error al guardar el dominio'})
                else:
                    return JsonResponse({'error': 'No esta permitido'})
            else:
                return JsonResponse({'error': 'El usuario no esta autenticado'})
        except Exception as e:
            return JsonResponse({'error': 'Error al crear el dominio'})
    else:
        return JsonResponse({'error': 'El usuario no esta autenticado'})

def guardar_dominio(ob1, ob2, ob3, ob4, ob5):
    try: 
        dominio = Dominio.objects.create(
            nombre=ob1,
            identificador_dominio=ob2,
            descripcion=ob3,
            portada_dominio=ob4,
            usuario=ob5
            )
        # Añadimos a contenido
        dominio.save()
        return True
    except Exception as e:
        return False

def nombre_dominio_exist(ob1):
    try:
        if Dominio.objects.filter(nombre__iexact=ob1).exists():
            return True
    except Dominio.DoesNotExist:
        return False
    return False

# METODO DE REGISTRO DE CONTENIDO
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def api_contenido_register(request):
    if request.user.is_authenticated:
        try:
            # Decodifica el token
            token = request.headers.get('Authorization').split(" ")[1]
            user = get_user_from_token_jwt(token)
            #user = get_user_from_token(token)
            # Validamos si el usuario es tecnico
            if is_tecnico(user):
                # Verificar si el usuario existe
                if request.method == 'POST' and user:
                    nombre_contenido_ = request.POST.get('nombre')
                    dominio_ = request.POST.get('dominio_tipo')
                    portada_ = request.FILES.get('portada')
                    # Verificar si el nombre del contenido ya existe
                    if nombre_contenido_exist(nombre_contenido_):
                        return JsonResponse({'error': 'El nombre del contenido ya existe'})
                    else:
                        # Calculamos el identificador
                        identificador_ = generar_identificador_contenido()
                        # Obtenemos el objeto dominio por el nombre
                        dominio__ob = Dominio.objects.get(nombre=dominio_)
                        # Creamos el contenido
                        if guardar_contenido(nombre_contenido_, identificador_, dominio_, portada_, dominio__ob):
                            return JsonResponse({'success': True})
                        else:
                            return JsonResponse({'error': 'Error al guardar el contenido'})
                else:
                    return JsonResponse({'error': 'No esta permitido'})
            else:
                return JsonResponse({'error': 'El usuario no esta autenticado'})
        except Exception as e:
            return JsonResponse({'error': 'Error al crear el contenido'})
    else:
        return JsonResponse({'error': 'El usuario no esta autenticado'})

def guardar_contenido(ob1, ob2, ob3, ob4, ob5):
    try:
        contenido = Contenido.objects.create(
            nombre=ob1,
            identificador_contenido=ob2,
            dominio_tipo=ob3,
            portada=ob4,
            dominio=ob5
        )
        # Añadimos a contenido
        contenido.save()
        return True
    except Exception as e:
        return False

def nombre_contenido_exist(ob1):
    try:
        if Contenido.objects.filter(nombre__iexact=ob1).exists():
            return True
    except Contenido.DoesNotExist:
        return False
    return False

# METODO DE REGISTRO DE CONTENIDO INDIVIDUAL
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def api_contenido_individual_register(request):
    if request.user.is_authenticated:
        try:
            # Decodifica el token
            token = request.headers.get('Authorization').split(" ")[1]
            user = get_user_from_token_jwt(token)
            #user = get_user_from_token(token)
            # Validamos si el usuario es tecnico
            if is_tecnico(user):
                if request.method == 'POST' and user:
                    descripcion_ = request.POST.get('descripcion_individual')
                    tipocontenido_ = request.POST.get('tipo_contenido')
                    respuesta_ = request.POST.get('respuesta')
                    contenido_ = request.FILES.get('contenido_individual')
                    portada_ = request.FILES.get('portada_individual')
                    pertenece_ = request.POST.get('conten')
                    nombre_nivel_ = request.POST.get('nombre_nivel')
                    # Obtenemos el objeto contenido por el nombre
                    contenido__ob = Contenido.objects.get(nombre=pertenece_)
                    # Calculamos el identificador
                    identificador_ = generar_identificador_individual()
                    # Creamos el contenido
                    if guardar_contenido_individual(descripcion_, identificador_, tipocontenido_, contenido_, 
                                                    portada_, respuesta_, nombre_nivel_, contenido__ob):
                        return JsonResponse({'success': True})
                    else:
                        return JsonResponse({'error': 'Error al guardar el contenido individual'})
                else:
                    return JsonResponse({'error': 'Error al guardar el contenido'})
            else:
                return JsonResponse({'error': 'El usuario no esta autenticado'})
        except Exception as e:
            return JsonResponse({'error': 'Error al crear el contenido individual'})
    else:
        return JsonResponse({'error': 'El usuario no esta autenticado'})

def guardar_contenido_individual(ob1, ob2, ob3, ob4, ob5, ob6, ob7, ob8):
    try:
        contenido_individual = ContenidoIndividual.objects.create(
            descripcion_individual=ob1,
            identificador_individual=ob2,
            tipo_contenido=ob3,
            contenido_individual=ob4,
            portada_individual=ob5,
            respuesta=ob6,
            nivel=ob7,
            contenido=ob8
        )
        # Añadimos a contenido
        contenido_individual.save()
        return True
    except Exception as e:
        return False

# METODO DE REGISTRO EN CURSO
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def api_curso_inscripcion(request, id):
    try:
         # Verificar existencia de token
        token = request.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        #user = get_user_from_token(token)
        if is_paciente(user):
            # Encontrar el paciente del user
            paciente__ob = Paciente.objects.get(user=user)
            # Encontrar el curso en base al id
            curso__ob = Curso.objects.get(id=id)
            # Verificar si el curso existe
            if curso__ob:
                # Creamos el detalle de inscripcion
                if guardar_inscripcion(paciente__ob, curso__ob):
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'error': 'No pudo inscribirse'}, status=500)
        else:
            return JsonResponse({'errorSalida': 'El usuario no esta autenticado'}, status=401)
    except Exception as e:
        return JsonResponse({'errorSalida': str(e)}, status=500)

def guardar_inscripcion(ob1, ob2):
    try:
        detalle_inscripcion = DetalleInscripcionCurso.objects.create(
            paciente=ob1,
            curso=ob2
        )
        # Añadimos a contenido
        detalle_inscripcion.save()
        return True
    except Exception as e:
        return False

# VERIFICACION DE INSCRIPCION
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def verificacion_inscripcion(request):
    try:
         # Verificar existencia de token
        token = request.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        #user = get_user_from_token(token)
        if is_paciente(user):
            # Encontrar el paciente del user
            paciente__ob = Paciente.objects.get(user=user)
            # Encontrar el curso en base al id
            detalle__inscripcion = DetalleInscripcionCurso.objects.filter(paciente=paciente__ob)
            # Verificar si el curso existe
            if detalle__inscripcion:
                context = {
                    'success': True,
                    'inscrito': "1"
                }
                return JsonResponse(context)
            else:
                context = {
                    'success': True,
                    'inscrito': "0"
                }
                return JsonResponse(context)
        else:
            return JsonResponse({'error': 'El usuario no esta autenticado'}, status=401)
    except Exception as e:
        return JsonResponse({'errorSalida': str(e)}, status=500)



# METODO DE REGISTRO DE CURSO
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def api_curso_register(request):
    if request.user.is_authenticated:
        try:
            # Decodifica el token
            token = request.headers.get('Authorization').split(" ")[1]
            user = get_user_from_token_jwt(token)
            #user = get_user_from_token(token)
            # Validamos si el usuario es comun
            if is_comun(user):
                print("Pasamos el if")
                if request.method == 'POST' and user:
                    data = json.loads(request.body)
                    nombre_curso_ = data.get('nombre_curso')
                    descripcion_ = data.get('descripcion')
                    # Verificar si el nombre del curso ya existe
                    if nombreCurso_exist(nombre_curso_):
                        return JsonResponse({'error': 'El nombre del curso ya existe'})
                    else:
                        # Calculamos el identificador
                        identificador_ = generar_identificador_curso()
                        comun__ob = UsuarioComun.objects.get(user=user)
                        # Creamos el curso
                        if guardar_curso(nombre_curso_, descripcion_, identificador_, comun__ob):
                            return JsonResponse({'success': True})
                        else:
                            return JsonResponse({'error': 'No es posible crear el curso'})
                else:
                    return JsonResponse({'error': 'Error al crear el curso'})
            else:
                return JsonResponse({'error': 'El usuario no esta autenticado'})
        except Exception as e:
            return JsonResponse({'error': 'Error al crear el curso'})
    else:
        return JsonResponse({'error': 'El usuario no esta autenticado'})

def guardar_curso(ob1, ob2, ob3, ob4):
    try:
        curso = Curso.objects.create(
            nombre_curso=ob1,
            descripcion_curso=ob2,
            identificador_curso=ob3,
            usuario_comun=ob4
        )
        # Añadimos a contenido
        curso.save()
        return True
    except Exception as e:
        return False

def nombreCurso_exist(ob1):
    try:
        if Curso.objects.filter(nombre_curso__iexact=ob1).exists():
            return True
    except Curso.DoesNotExist:
        return False
    return False


# METODO DE COMPORBAR SI HAY COMA
def comprobar_separacion_coma(valor_respuesta):
    # Verificar si el string contiene una coma
    if ',' in valor_respuesta:
        return True  # Si hay una coma, entonces hay varios valores
    else:
        return False  # Si no hay una coma, entonces solo hay un valor


# METODO DE OBTENER CONTENIDO
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def contenido_individual(request, slug):
    try:
        # Decodifica el token
        token = request.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        #user = get_user_from_token(token)
        if (user and token):
            # Obtenemos los objetos de Contenido
            contenidoI__ob = ContenidoIndividual.objects.get(
                slug_contenido_individual=slug)
            contenido__ob = contenidoI__ob.contenido
            # obtenemos la url de contenido
            if contenidoI__ob.contenido_individual:
                # Variable contenedor
                contenedor = ""
                url__contenido = cloudinary.CloudinaryImage(
                    contenidoI__ob.contenido_individual.name).build_url()
                # Obtener los valores requeridos
                nombre__contenido = contenido__ob.nombre
                descripcion__contenido = contenidoI__ob.descripcion_individual
                identificador = contenidoI__ob.identificador_individual
                valor_respuesta = contenidoI__ob.respuesta
                # Obtener el tipo de contenido
                tipo__contenido = contenido__ob.dominio_tipo
                # Comprobar si existe una sola descripcion o varias
                if comprobar_separacion_coma(descripcion__contenido):
                    descripcion_separada = descripcion__contenido.split(', ')
                    descripcion__contenido = descripcion_separada
                else:
                    descripcion__contenido = descripcion__contenido
                # Comprobar si existe una sola respuesta o varias
                if comprobar_separacion_coma(valor_respuesta):
                    valores_separados = valor_respuesta.split(', ')
                    valores_separados = [valor.capitalize()
                                         for valor in valores_separados]
                    contenedor = valores_separados
                    context = {'url__contenido': url__contenido, 'contenedor': contenedor,
                               'nombre__contenido': nombre__contenido, 'descripcion__contenido': descripcion__contenido, 'identificador': identificador,
                               'tipo__contenido': tipo__contenido, 'slug': slug}
                else:
                    contenedor = valor_respuesta
                    context = {'url__contenido': url__contenido, 'contenedor': contenedor,
                               'nombre__contenido': nombre__contenido, 'descripcion__contenido': descripcion__contenido, 'identificador': identificador,
                               'tipo__contenido': tipo__contenido, 'slug': slug}

                # Determinar el tipo de contenido y renderizar la plantilla adeacuada al tipo
                if (contenidoI__ob.tipo_contenido == 'selecion_individual'):
                    context.update({'tipo': 'selecion_individual'})
                    return JsonResponse(context)
                elif (contenidoI__ob.tipo_contenido == 'verdadero_falso'):
                    context.update({'tipo': 'verdadero_falso'})
                    return JsonResponse(context)
                elif (contenidoI__ob.tipo_contenido == 'selecion_multiple'):
                    context.update({'tipo': 'selecion_multiple'})
                    return JsonResponse(context)
                elif (contenidoI__ob.tipo_contenido == 'responder_preguntas'):
                    context.update({'tipo': 'responder_preguntas'})
                    return JsonResponse(context)
                elif (contenidoI__ob.tipo_contenido == 'cuento'):
                    context.update({'tipo': 'cuento'})
                    return JsonResponse(context)

            else:
                error_message = "No existe contenido"
                context = {
                    'errorNormal': error_message, 'slug': slug
                }
                return JsonResponse(context, status=404)
        else:
            return JsonResponse({'errorSalida': 'El usuario no esta autenticado'}, status=401)
    except ContenidoIndividual.DoesNotExist:
        error = "No existe contenido"
        contexto_dos = {'errorNormal': error, 'slug': slug}
        return JsonResponse(contexto_dos, status=404)

    except Exception as e:
        return JsonResponse({'errorSalida':'Ups, Algo salió mal'}, status=500)


# METODO DE OBTENER CONTENIDO PRINCIPAL
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def contenido_principal(request, slug):
    # Decodifica el token
    token = request.headers.get('Authorization').split(" ")[1]
    user = get_user_from_token_jwt(token)
    #user = get_user_from_token(token)
    if user and token:
        if request.method == 'GET':
            # Obtenemos el objeto dominio
            dominio__ob = Dominio.objects.get(slug_dominio=slug)
            context = {'identificador': dominio__ob.id, 'slug': slug}
            return JsonResponse(context)
        else:
            return JsonResponse({'error': 'Método no permitido'}, status=405)
    else:
        return JsonResponse({'error': 'Token no proporcionado'}, status=401)


# METODO DE REGISTRO DE RESULTADO
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def save_resultado(request):
    try:
        # Decodifica el token
        token = request.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        #user = get_user_from_token(token)
        if (is_paciente(user)):
            if request.method == 'POST':
                data = json.loads(request.body)
                tiempo_transcurrido_m = data.get('tiempoTranscurrido__minutos')
                tiempo_transcurrido_s = data.get('tiempoTranscurrido__segundos')
                respuesta__contenido = data.get('respuesta')
                slug__con = data.get('slug__')
                # Obtenemos el objeto contenido
                contenido__ob = ContenidoIndividual.objects.get(slug_contenido_individual=slug__con)
                # Obtenemos el objeto paciente
                paciente__ob = Paciente.objects.get(user=user)
                # Captura de respuesta
                if tiempo_transcurrido_m == 0 and tiempo_transcurrido_s == 0:
                    tiempo_transcurrido_m_ = 40
                    tiempo_transcurrido_s_ = 1
                    respuesta__contenido_ = "No resuelto"
                    observacion = "No resuelto"
                    # Guardamos el resultado
                    if guardar_resultado_no(
                        tiempo_transcurrido_m_, tiempo_transcurrido_s_, respuesta__contenido_,
                        observacion, contenido__ob, paciente__ob):
                        # Enviamos una respuesta al front
                        return JsonResponse({'success': True})
                    else:
                        error_message = "Error al agregar resultado."
                        context = {'error': error_message, 'success': False}
                        return JsonResponse(context)

                else:
                    if tiempo_transcurrido_m or tiempo_transcurrido_s:
                        # Guardamos el resultado
                        if guardar_resultado(tiempo_transcurrido_m, tiempo_transcurrido_s, 
                                          respuesta__contenido, contenido__ob, paciente__ob):
                            # Enviamos una respuesta al front
                            return JsonResponse({'success': True})
                        else:
                            error_message = "Error al agregar resultado."
                            context = {'error': error_message, 'success': False}
                            return JsonResponse(context)
                    else:
                        error_message = "Tiempo transcurrido no proporcionado."
                        context = {'error': error_message, 'success': False}
                        return JsonResponse(context)
            else:
                error_message = "Error al agregar resultado."
                context = {'error': error_message, 'success': False}
                return JsonResponse(context)
        else:
            return JsonResponse({'error': 'El usuario no esta autenticado'})
    except IntegrityError:
        error_message = "Error al agregar."
        context = {'error': error_message, 'success': False}
        return JsonResponse(context)

def guardar_resultado(ob1, ob2, ob3, ob4, ob5):
    try:
        resultado_obj = Resultado.objects.create(
            tiempo_m=ob1,
            tiempo_s=ob2,
            respuesta=ob3,
            contenido_individual=ob4,
            paciente=ob5
        )
        resultado_obj.save()
        return True
    except Exception as e:
        return False

def guardar_resultado_no(ob1, ob2, ob3, ob4, ob5, ob6):
    try:
        resultado_obj = Resultado.objects.create(
            tiempo_m=ob1,
            tiempo_s=ob2,
            respuesta=ob3,
            observacion=ob4,
            contenido_individual=ob5,
            paciente=ob6
        )
        resultado_obj.save()
        return True
    except Exception as e:
        return False


# METODO DE REGISTRO DE PETICION
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def api_peticion_register(request):
    if request.user.is_authenticated:
        try:
            # Decodifica el token para obtener el usuario
            token = request.headers.get('Authorization').split(" ")[1]
            user = get_user_from_token_jwt(token)
            #user = get_user_from_token(token)
            # Validamos si el usuario es tecnico
            if is_comun(user):
                # Encontrar al usuario relacionado al user
                usuario__ob = UsuarioComun.objects.get(user=user)
                # Verificar si el usuario existe
                if request.method == 'POST' and usuario__ob:
                    motivo_peticion_ = request.POST.get('motivo')
                    tipo_peticion_ = request.POST.get('tipo')
                    peticion_cuerpo_ = request.POST.get('peticion_cuerpo')
                    # Creamos el contenido
                    if guardar_peticion(motivo_peticion_, tipo_peticion_, peticion_cuerpo_, usuario__ob):
                    # Actualizamos el contador
                        contador_obj, created = ContadorPeticiones.objects.get_or_create(pk=1)
                        contador_obj.contador += 1
                        contador_obj.save()
                        # Enviamos una respuesta al front
                        return JsonResponse({'success': True})
                    else:
                        return JsonResponse({'error': 'No se pudo guardar la petición'})
                else:
                    return JsonResponse({'error': 'Algo no es esta permitido'})
            else:
                return JsonResponse({'error': 'El usuario no esta autenticado'})
        except Exception as e:
            return JsonResponse({'error': 'Error al crear la petición'})
    else:
        return JsonResponse({'error': 'El usuario no esta autenticado'})

def guardar_peticion(ob1, ob2, ob3, ob4):
    try:
        peticion = Peticion.objects.create(
            motivo_peticion=ob1,
            tipo_peticion=ob2,
            peticion_cuerpo=ob3,
            usuario_comun=ob4
        )
        # Añadimos a peticion
        peticion.save()
        return True
    except Exception as e:
        return False

# METODO PARA ATENER PETICION Y ENVIAR CORREO
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def atender_peticion(request):
    try:
        # Decodifica el token
        token = request.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        #user = get_user_from_token(token)
        if is_tecnico(user):
            if request.method == 'POST':
                data = json.loads(request.body)
                slug = data.get('slug')
                estadoR_ = data.get('estadoR')
                vereficto_ = data.get('vereficto')
                if atención_peticion(slug):
                    # Enviamos el email antes de modificar
                    peticion__ob = Peticion.objects.get(slug_peticion=slug)
                    tecnico__ob = Usuario.objects.get(user=user)                    
                    if send_email(peticion__ob, vereficto_, estadoR_):
                        try:
                            # Agregamos detalle de peticion
                            if guardar_detalle(peticion__ob.motivo_peticion, tecnico__ob, peticion__ob):
                                # Actualizamos el contador de ContadorPeticionesAtendidas
                                contador_obj, created = ContadorPeticionesAtendidas.objects.get_or_create(usuario_comun=peticion__ob.usuario_comun)
                                contador_obj.contador += 1
                                contador_obj.save()
                                # Enviamos la respuesta al front
                                return JsonResponse({'success': True})
                            else:
                                return JsonResponse({'error': 'Error al guardar el detalle'}, status=500)
                        except Exception as e:
                            # Aquí puedes agregar logging o imprimir el error si es necesario
                            return JsonResponse({'error': 'Error al guardar el detalle'}, status=500)
                    else:
                        return JsonResponse({'error': 'Error al enviar el email'}, status=400)
                else:
                    return JsonResponse({'error': 'Error al atender la petición'}, status=400)
            else:
                return JsonResponse({'error': 'Algo no esta permitido'}, status=405)
        else:
            return JsonResponse({'errorSalida': 'El usuario no esta autenticado'}, status=401)
    except Peticion.DoesNotExist:
        error = "No existe petición"
        contexto_dos = {'error': error, 'slug': slug}
        return JsonResponse(contexto_dos)
    except Exception as e:
        return JsonResponse({'error': 'Ups! Algo salió mal'}, status=500)

def atención_peticion(ob1):
    try: 
        # Obtenemos el objeto peticions
        peticion__ob = Peticion.objects.get(slug_peticion=ob1)
        # Modificamos el estado de revisión
        peticion__ob.estado_revision = True
        # Guardamos los datos y verificar si se guardaron
        peticion__ob.save()
        return True
    except Exception as e:
        return False

def guardar_detalle(ob1, ob2, ob3):
    try:
        detalle_peticion = DetallePeticion.objects.create(
            motivo_peticion=ob1,
            usuario_tecnico=ob2,
            peticion=ob3
        )
        # Añadimos a contenido
        detalle_peticion.save()
        # Correo

        return True
    except Exception as e:
        return False

def send_email(peticion__ob, ob1, ob2):
    # Capturamos los datos para el email
    subject = 'Notificación de revisión de petición'
    message = ('Su petición de tipo ' + peticion__ob.tipo_peticion + 
               ' ha sido atendida.\n' +
               'El motivo de la misma era: ' + peticion__ob.motivo_peticion + 
               '\nEl verdicto de la revisión es : ' + ob1 +
               '\nLa misma cuenta con un estado de : ' + ob2) 
    from_email = settings.EMAIL_HOST_USER
    #receiver_email = ['cristobal.rios@unl.edu.ec']
    #receiver_email= ['genoveva.suing@unl.edu.ec']
    receiver_email = [peticion__ob.usuario_comun.email_usuario]

    send_mail(subject, message, from_email, receiver_email, fail_silently=False)
    return True


## METODO DE OBTENER EL NUMERO DE PETICIONES NUEVAS AGREGADAS
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_contador_peticiones(request):
    if request.method == 'GET':
        contador_obj = ContadorPeticiones.objects.get(pk=1)
        return JsonResponse({'contador': contador_obj.contador})
    else:
        return JsonResponse({'error': 'No hay contador'}, status=405)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def reset_contador_peticiones(request):
    if request.method == 'GET':
        contador_obj = ContadorPeticiones.objects.get(pk=1)
        contador_obj.contador = 0
        contador_obj.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'No se puede resetear contador'}, status=405)


## METODO DE OBTENER EL NUMERO DE PETICIONES ATENDIDAS
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_contador_peticiones_atendidas(request):
    try:
        if request.method == 'GET':
            # Decodifica el token
            token = request.headers.get('Authorization').split(" ")[1]
            user = get_user_from_token_jwt(token)
            if (is_comun(user)):
                # Obtenemos el objeto usuario comun
                usuario__ob = UsuarioComun.objects.get(user=user)
                # Filtramos el contador del usuariuo comun
                contador_obj = ContadorPeticionesAtendidas.objects.get(usuario_comun=usuario__ob)
                return JsonResponse({'contador': contador_obj.contador})
            else:
                return JsonResponse({'error': 'Token no proporcionado'}, status=401)
        else:
            return JsonResponse({'error': 'Método no permitido'}, status=405) 
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500) 

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def reset_contador_peticiones_atendidas(request):
    try:
        if request.method == 'GET':
            # Decodifica el token
            token = request.headers.get('Authorization').split(" ")[1]
            user = get_user_from_token_jwt(token)
            if (is_comun(user)):
                # Obtenemos el objeto usuario comun
                usuario__ob = UsuarioComun.objects.get(user=user)
                # Filtramos el contador del usuariuo comun
                contador_obj = ContadorPeticionesAtendidas.objects.get(usuario_comun=usuario__ob)
                contador_obj.contador = 0
                contador_obj.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'Token no proporcionado'}, status=401)
        else:
            return JsonResponse({'error': 'Método no permitido'}, status=405) 
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500) 



## METODO DE REGISTRO DE SALA
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def api_sala_register_new(request):
    try:
        # Decodifica el token para obtener el usuario
        token = request.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        #user = get_user_from_token(token)
        # Validamos si el usuario es tecnico
        if is_comun(user):
            # Encontrar al usuario relacionado al user
            usuario__ob = UsuarioComun.objects.get(user=user)
            # Verificar si el usuario existe
            if request.method == 'POST' and usuario__ob:
                data = json.loads(request.body)
                nombre_sala_ = data.get('nombre_sala')
                nombre_sala_n_ = data.get('nombre_sala_n')
                anotaciones_ = data.get('anotaciones')
                codigo_identificador_ = data.get('codigo_identificador')
                nombre_paciente_ = data.get('nombre_paciente')
                # Obtener el nombre y apellido del paciente de nombre_paciente
                nombres_divididos = nombre_paciente_.split(' ')
                nombre = nombres_divididos[0]
                apellido = nombres_divididos[1]
                # Verificar que exista curso para el usuario
                if curso_existe(usuario__ob):
                    # Verificar si el paciente existe
                    if paciente_existe(nombre, apellido):
                        # Obtener el paciente
                        paciente_ob = Paciente.objects.get(nombre_usuario__iexact=nombre, apellido_usuario__iexact=apellido)
                        # Verificar si el paciente existe en el curso
                        if paciente_existe_curso(paciente_ob, usuario__ob):
                            # Verificar si el identificador existe
                            if identificador_existe(codigo_identificador_):
                                # Creamos la sala
                                if nombresala_exist(nombre_sala_):
                                    error_message = "El nombre de la sala ya existe. Ingresa otro nombre."
                                    context = {'error': error_message}
                                    return JsonResponse(context)
                                else:
                                    if guardar_sala(nombre_sala_, anotaciones_, codigo_identificador_, usuario__ob, paciente_ob):
                                        # Actualizamos el contador
                                        contador_obj, created = ContadorSalas.objects.get_or_create(paciente=paciente_ob)
                                        contador_obj.contador += 1
                                        contador_obj.save()
                                        # Enviamos una respuesta al front
                                        return JsonResponse({'success': True})
                                    else:
                                        error_message = "Error al agregar sala."
                                        context = {'error': error_message}
                                        return JsonResponse(context)
                            else:
                                error_message = "El contenido que requiere evaluar no existe. Ingresa un identificador válido."
                                context = {'error': error_message}
                                return JsonResponse(context)
                        else:
                            error_message = "El paciente no se encuentra inscrito en un curso o no existe."
                            context = {'error': error_message}
                            return JsonResponse(context)
                    else:
                        context = {'error': 'El paciente no existe.'}
                        return JsonResponse(context)
                else:
                    error_message = "No tiene un curso registrado. No puede registrar salas."
                    context = {'error': error_message}
                    return JsonResponse(context)
            else:
                return JsonResponse({'error': 'Algo no esta permitido'})
        else:
            return JsonResponse({'error': 'El usuario no esta autenticado'})
    except Exception as e:
        print(e)
        return JsonResponse({'error': "Algo salio mal"})


## METODO DE REGISTRO DE SALA
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def api_sala_register(request):
    if request.user.is_authenticated:
        try:
            token = request.headers.get('Authorization').split(" ")[1]
            user = get_user_from_token_jwt(token)
        except Exception as e:
            return JsonResponse({'error': 'El usuario no está autenticado'})

        # Verifica si el usuario es técnico.
        if not is_comun(user):
            return JsonResponse({'error': 'El usuario no está autenticado'})

        # Encontrar al usuario relacionado al user
        try:
            usuario__ob = UsuarioComun.objects.get(user=user)
        except UsuarioComun.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'})

        if request.method != 'POST':
            return JsonResponse({'error': 'Método no permitido'})

        data = json.loads(request.body)
        nombre_sala_ = data.get('nombre_sala')
        anotaciones_ = data.get('anotaciones')
        codigo_identificador_ = data.get('codigo_identificador')
        nombre_paciente_ = data.get('nombre_paciente')
        nombres_divididos = nombre_paciente_.split(' ')
        nombre = nombres_divididos[0]
        apellido = nombres_divididos[1]

        if not curso_existe(usuario__ob):
            return JsonResponse({'error': "No tiene un curso registrado. No puede registrar salas."})

        if not paciente_existe(nombre, apellido):
            return JsonResponse({'error': 'El paciente no existe.'})

        paciente__ob = Paciente.objects.get(nombre_usuario__iexact=nombre, apellido_usuario__iexact=apellido)

        if not paciente_existe_curso(paciente__ob, usuario__ob):
            return JsonResponse({'error': "El paciente no se encuentra inscrito en un curso o no existe."})

        if not identificador_existe(codigo_identificador_):
            return JsonResponse({'error': "El contenido que requiere evaluar no existe. Ingresa un identificador válido."})

        if nombresala_exist(nombre_sala_):
            return JsonResponse({'error': "El nombre de la sala ya existe. Ingresa otro nombre."})
        
        try: 
            if guardar_sala(nombre_sala_, anotaciones_, codigo_identificador_, usuario__ob, paciente__ob):
                # Actualizamos el contador
                contador_obj, created = ContadorSalas.objects.get_or_create(paciente=paciente__ob)
                contador_obj.contador += 1
                contador_obj.save()
                # Enviamos una respuesta al front
                return JsonResponse({'success': True})
            else:
                error_message = "Error al agregar sala."
                context = {'error': error_message}
                return JsonResponse(context)
        except Exception as e:
            print(e)
            return JsonResponse({'error': "Algo salió mal"})
    else:
        return JsonResponse({'error': 'El usuario no está autenticado'})


def guardar_sala (ob1, ob2, ob3, ob4, ob5):
    try:
        sala_obj = Sala.objects.create(
            nombre_sala=ob1,
            anotaciones=ob2,
            codigo_identificador=ob3,
            paciente=ob5
        )
        sala_obj.save()
        # Creamos el detalle de sala
        detalle_obj = DetalleSala.objects.create(
            sala = sala_obj,
            usuario_comun=ob4
        )
        detalle_obj.save()
        return True
    except Exception as e:
        return False


def paciente_existe_curso(paciente_ob, usuario_ob):
    try:
        # validamos la existencia
        if DetalleInscripcionCurso.objects.filter(paciente=paciente_ob, curso__usuario_comun=usuario_ob).exists():
            return True
    except DetalleInscripcionCurso.DoesNotExist:
        return False
    return False
    

def curso_existe(usuario_ob):
    try:
        cursos = Curso.objects.filter(usuario_comun=usuario_ob)
        if not cursos.exists():
            return False
        for curso in cursos:
            inscripciones = DetalleInscripcionCurso.objects.filter(curso=curso, curso__usuario_comun=usuario_ob).exists()
            if inscripciones:
                return True
        return False
    except Exception as e:
        return False
    

def paciente_existe(nombre, apellido):
    try:
        # buscamos al paciente mediante el nombre y apellido proporcionado
        if Paciente.objects.filter(nombre_usuario__iexact=nombre, apellido_usuario__iexact=apellido).exists():
            return True
    except Paciente.DoesNotExist:
        return False
    return False


def identificador_existe(ob1):
    try:
        # buscamos al paciente mediante el nombre y apellido proporcionado
        if ContenidoIndividual.objects.filter(identificador_individual__iexact=ob1).exists():
            return True
    except ContenidoIndividual.DoesNotExist:
        return False
    return False


def nombresala_exist(ob1):
    try:
        if Sala.objects.filter(nombre_sala__iexact=ob1).exists():
            return True
    except Sala.DoesNotExist:
        return False
    return False


## CONTADOR DE SALAS 
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_contador_salas(request):
    try:
        if request.method == 'GET':
            # Decodifica el token
            token = request.headers.get('Authorization').split(" ")[1]
            user = get_user_from_token_jwt(token)
            if (is_paciente(user)):
                if paciente_existe_contador(user):
                    contador = numero_contador(user)
                    return JsonResponse({'contador': contador})
                else:
                    return JsonResponse({'contador': 0})
            else:
                return JsonResponse({'error': 'El usuario no esta autenticado'}, status=401)
        else:
            return JsonResponse({'error': 'Algo no esta permitido'}, status=405) 
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500) 

def numero_contador(user):
    try:
        # Obtenemos el objeto usuario comun
        usuario__ob = Paciente.objects.get(user=user)
        # Filtramos el contador del usuariuo comun
        contador_obj = ContadorSalas.objects.get(paciente=usuario__ob)
        return contador_obj.contador
    except ContadorSalas.DoesNotExist:
        return 0

def paciente_existe_contador(user):
    try:
        # Obtenemos el objeto usuario comun
        usuario__ob = Paciente.objects.get(user=user)
        # Filtramos el contador del usuariuo comun
        contador_ = ContadorSalas.objects.get(paciente=usuario__ob)
        return True
    except ContadorSalas.DoesNotExist:
        return False

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def reset_contador_salas(request):
    try:
        if request.method == 'GET':
            # Decodifica el token
            token = request.headers.get('Authorization').split(" ")[1]
            user = get_user_from_token_jwt(token)
            if (is_paciente(user)):
                # Obtenemos el objeto usuario comun
                usuario__ob = Paciente.objects.get(user=user)
                # Filtramos el contador del usuariuo comun
                contador_obj = ContadorSalas.objects.get(paciente=usuario__ob)
                contador_obj.contador = 0
                contador_obj.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'El usuario no esta autenticado'}, status=401)
        else:
            return JsonResponse({'error': 'Algo no esta permitido'}, status=405) 
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500) 


## ATENDER SALA ###
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def atender_sala(request, slug):
    try:
        # Decodifica el token
        token = request.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        #user = get_user_from_token(token)
        if is_paciente(user):
            if request.method == 'GET':
                if modificar_estado_sala(slug):
                    return JsonResponse({'success': True})
                else:
                    error_message = "Error al modificar el estado de la sala."
                    context = {'error': error_message}
                    return JsonResponse(context)
            else:
                return JsonResponse({'error': 'Algo no esta permitido'}, status=405)
        else:
            return JsonResponse({'error': 'El usuario no esta autenticado'}, status=401)
    except Peticion.DoesNotExist:
        error = "No existe sala"
        contexto_dos = {'error': error, 'slug': slug}
        return JsonResponse(contexto_dos)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def modificar_estado_sala(slug):
    try:
        # Obtenemos el objeto sala
        sala__ob = Sala.objects.get(slug_sala=slug)
        # Modificamos el estado de la sala
        sala__ob.sala_atendida = True
        # Guardamos los datos y verificar si se guardaron
        sala__ob.save()
        # Actualizamos el contador
        ob_detalle = DetalleSala.objects.get(sala=sala__ob)
        # Encontrar el usuario comun que creo la sala
        usuario_comun = ob_detalle.usuario_comun
        contador_obj, created = ContadorSalasAtendidas.objects.get_or_create(usuario_comun=usuario_comun)
        contador_obj.contador += 1
        contador_obj.save()
        if send_email_sala(sala__ob, usuario_comun):
            return True
        else:
            return False
    except Exception as e:
        return False


def send_email_sala(ob1, ob2):
    # Capturamos los datos para el email
    subject = 'Notificación de resolución de sala'
    message = ('La sala creada de nombre ' + ob1.nombre_sala + 
               ' ha sido atendida por el paciente ' + ob1.paciente.nombre_usuario + ' ' + ob1.paciente.apellido_usuario + '\n' +
               'La descripción de la misma era: ' + ob1.anotaciones + 
               '\nLa misma cuenta con un estado de : Resuelto') 
    from_email = settings.EMAIL_HOST_USER
    #receiver_email = ['cristobal.rios@unl.edu.ec']
    #receiver_email= ['genoveva.suing@unl.edu.ec']
    receiver_email = [ob2.email_usuario]

    send_mail(subject, message, from_email, receiver_email, fail_silently=False)
    return True

## CONTADOR DE SALAS ATENDIDAS
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_contador_salas_atendidas(request):
    try:
        if request.method == 'GET':
            # Decodifica el token
            token = request.headers.get('Authorization').split(" ")[1]
            user = get_user_from_token_jwt(token)
            if (is_comun(user)):
                if comunN_existe_contador(user):
                    contador = numero_contador_SA(user)
                    return JsonResponse({'contador': contador})
                else:
                    return JsonResponse({'contador': 0})
            else:
                return JsonResponse({'error': 'El usuario no esta autenticado'}, status=401)
        else:
            return JsonResponse({'error': 'Algo no esta permitido'}, status=405) 
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500) 

def comunN_existe_contador(user):
    try:
        # Obtenemos el objeto usuario comun
        usuario__ob = UsuarioComun.objects.get(user=user)
        # Filtramos el contador del usuariuo comun
        if ContadorSalasAtendidas.objects.filter(usuario_comun=usuario__ob).exists():
            return True
    except ContadorSalasAtendidas.DoesNotExist:
        return False
    return False

def numero_contador_SA(user):
    try:
        # Obtenemos el objeto usuario comun
        usuario__ob = UsuarioComun.objects.get(user=user)
        # Filtramos el contador del usuariuo comun
        contador_obj = ContadorSalasAtendidas.objects.get(usuario_comun=usuario__ob)
        return contador_obj.contador
    except ContadorSalasAtendidas.DoesNotExist:
        return 0


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def reset_contador_salas_atendidas(request):
    try:
        if request.method == 'GET':
            # Decodifica el token
            token = request.headers.get('Authorization').split(" ")[1]
            user = get_user_from_token_jwt(token)
            if (is_comun(user)):
                # Obtenemos el objeto usuario comun
                usuario__ob = UsuarioComun.objects.get(user=user)
                # Filtramos el contador del usuariuo comun
                contador_obj = ContadorSalasAtendidas.objects.get(usuario_comun=usuario__ob)
                contador_obj.contador = 0
                contador_obj.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'El usuario no esta autenticado'}, status=401)
        else:
            return JsonResponse({'error': 'Algo no esta permitido'}, status=405) 
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500) 


## OBTENER SLUG DE CONTENIDO ###
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def obtener_contenido_individual(request, codigo):
    try:
        # Decodifica el token
        token = request.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        #user = get_user_from_token(token)
        if is_paciente(user):
            if request.method == 'GET':
                codigo_ = codigo
                slug = obtener_slug_CI(codigo_)
                if slug:
                    return JsonResponse({'success': True, 'slug': slug})
                else:
                    error_message = "El contenido no existe."
                    context = {'error': error_message}
                    return JsonResponse(context)
            else:
                return JsonResponse({'error': 'No es posible ejecutar la acción'}, status=405)
        else:
            return JsonResponse({'error': 'El usuario no se ha autenticado'}, status=401)
    except Exception as e:
        return JsonResponse({'error': 'Ups! algo salió mal'}, status=500)

def obtener_slug_CI(codigo):
    try:
        # Obtenemos el objeto contenido individual
        contenidoI__ob = ContenidoIndividual.objects.get(identificador_individual=codigo)
        # Obtenemos el slug
        slug = contenidoI__ob.slug_contenido_individual
        return slug
    except ContenidoIndividual.DoesNotExist:
        return False


## OBTENER SLUG DE SLUG DE CURSO ###
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def obtener_slug_curso(request, id):
    try: 
        # Decodifica el token
        token = request.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        #user = get_user_from_token(token)
        if is_comun(user):
            if request.method == 'GET':
                id_ = id
                slug = obtener_slug(id_)
                if slug:
                    return JsonResponse({'success': True, 'slug': slug})
                else:
                    error_message = "El curso no existe."
                    context = {'error': error_message}
                    return JsonResponse(context)
            else:
                return JsonResponse({'error': 'No es posible ejecutar la acción'}, status=405)
        else:
            return JsonResponse({'error': 'El usuario no se ha autenticado'}, status=401)
    except Exception as e:
        return JsonResponse({'error': 'Ups! algo salió mal'}, status=500)

def obtener_slug(id):
    try:
        # Obtenemos el obtjeto paciente con el id
        paciente__ob = Paciente.objects.get(id=id)
        # Obtenemos el registro de inscripcion a curso asociado
        detalle_inscripcion_curso = DetalleInscripcionCurso.objects.get(paciente=paciente__ob)
        # Obtener el curso asociado a esa inscripcion de paciente
        curso__ob = detalle_inscripcion_curso.curso
        # sacar el slug del curso
        slug = curso__ob.slug_curso
        return slug
    except Paciente.DoesNotExist:
        return False
    except DetalleInscripcionCurso.DoesNotExist:
        return False

## OBTENER SLUG DE SLUG DE DOMINIO ###
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def obtener_slug_dominio(request, slug):
    try: 
        # Decodifica el token
        token = request.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        #user = get_user_from_token(token)
        if user and token:
            if request.method == 'GET':
                slug_ = slug
                slug = obtener_slug_domi(slug_)
                if slug:
                    return JsonResponse({'success': True, 'slug_dominio': slug})
                else:
                    error_message = "El curso no existe."
                    context = {'error': error_message, 'success': False}
                    return JsonResponse(context)
            else:
                return JsonResponse({'error': 'No es posible ejecutar la acción'}, status=405)
        else:
            return JsonResponse({'error': 'El usuario no se ha autenticado'}, status=401)
    except Exception as e:
        return JsonResponse({'error': 'Ups! algo salió mal'}, status=500)

def obtener_slug_domi(ob1):
    try:
        # Obtenemos el obtjeto contenido con el slug
        contenido_ob = Contenido.objects.get(slug_contenido=ob1)
        # Obtenemos el dominio del contenido
        dominio = contenido_ob.dominio
        # sacar el slug del dominio
        slug = dominio.slug_dominio
        return slug
    except Contenido.DoesNotExist:
        return False
    except Dominio.DoesNotExist:
        return False
    

## OBTENER SLUG DE SLUG DE CONTENIDO ###
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def obtener_slug_contenido(request, slug):
    try: 
        # Decodifica el token
        token = request.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        #user = get_user_from_token(token)
        if user and token:
            if request.method == 'GET':
                slug_ = slug
                slug = obtener_slug_conte(slug_)
                if slug:
                    return JsonResponse({'success': True, 'slug_contenido': slug})
                else:
                    error_message = "El contenido no existe."
                    context = {'error': error_message, 'success': False}
                    return JsonResponse(context)
            else:
                return JsonResponse({'error': 'No es posible ejecutar la acción'}, status=405)
        else:
            return JsonResponse({'error': 'El usuario no se ha autenticado'}, status=401)
    except Exception as e:
        return JsonResponse({'error': 'Ups! algo salió mal'}, status=500)

def obtener_slug_conte(ob1):
    try:
        # Obtenemos el obtjeto individual con el slug
        contenido_ob = ContenidoIndividual.objects.get(slug_contenido_individual=ob1)
        # Obtenemos el contenido del individual
        contenido = contenido_ob.contenido
        # sacar el slug del dominio
        slug = contenido.slug_contenido
        return slug
    except ContenidoIndividual.DoesNotExist:
        return False
    except Contenido.DoesNotExist:
        return False
    
