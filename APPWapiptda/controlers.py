### GENERALES ###
from .models import *
from .serializer import *
from .views import *
### PAGINACION ###
from rest_framework.pagination import PageNumberPagination
### JWT ###
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import viewsets, generics

### CLASES DE PAGINACION ###
class Paginacion(PageNumberPagination):
    page_size = 8

class Paginacion2(PageNumberPagination):
    page_size = 6

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


### VISTAS DE USUARIO ###

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

""" Listados personalizados """

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