### GENERALES ###
from APPWapiptda.models import *
from APPWapiptda.serializer import *
from APPWapiptda.views import *
from EstudioyEntrenamiento.views import *
from datetime import datetime, timedelta
### PAGINACION ###
from rest_framework.pagination import PageNumberPagination
### JWT ###
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework import viewsets, generics

### CLASES DE PAGINACION ###
class Paginacion(PageNumberPagination):
    page_size = 8

class Paginacion2(PageNumberPagination):
    page_size = 6


""" Listados personalizados """

##### Lista de contenido que pertenece a un dominio especifico
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


##### Lista de contenido que pertenece a un dominio especifico sin paginacion
# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ContenidoIndividualTodoListView(generics.ListAPIView):
    serializer_class = ContenidIndividualSerializer
    def get_queryset(self):
        slug_contenido = self.kwargs['slug']
        contenidos = lista_actividades_contenido(slug_contenido)
        return contenidos


##### Lista de actividades que pertenencen a un tipo de contenido especifico
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


##### Lista de actividades que pertenencen a un nivel de TDAH especifico
##### permitiendo obtener una clara seperación de cada uno de ellos
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


##### Lista de los reportes que han sido generados por un usuario comun
##### pertimiendo obtener solo aquellos que ke pertenencen
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


##### Lista de peticiones con un estado de revision en False
##### es decir aquellas que aun no han sido atendidas
# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class PeticionListViewNo(generics.ListAPIView):
    serializer_class = PeticionSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        return Peticion.objects.filter(estado_revision=False)


##### Lista de peticiones con un estado de revision en True
# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class PeticionListViewSi(generics.ListAPIView):
    serializer_class = PeticionSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        return Peticion.objects.filter(estado_revision=True)


##### Lista de peticiones con un estado de revision en True 
##### pertenecientes a un usuario comun especifico
# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class PeticionUCListView(generics.ListAPIView):
    serializer_class = PeticionSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        return Peticion.objects.filter(usuario_comun=self.kwargs['id'])


##### Listado de pacientes pertenecientes a un curso especifio mediante
##### el id del curso
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


##### Detalle de resultados pertenecientes a un paciente especifico 
##### siempre y cuando este paciente este incripto en el curso
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


##### Detalle de resultados pertenecientes a un paciente especifico 
##### siempre y cuando este paciente este incripto en el curso mediante el nombre del paciente
# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ResultadodePacienteListView2(generics.ListAPIView):
    serializer_class = ResultadoSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Verificar el numero de elementos de la url en nombre
        if len(self.kwargs['nombre'].split(' ')) == 2:
            # Obtener nombre y apellido de la url
            nombre, apellido = self.kwargs['nombre'].split(' ', 1)
            if (nombre_paciente_exist(nombre , apellido)):
                # Filtrar registros de resultados por el nombre del paciente
                resultados = resultado_por_nombre(self.request, nombre, apellido)
                return resultados
            else:
                return []
        elif len(self.kwargs['nombre'].split(' ')) == 1:
            return []
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
    

##### Lista de peticiones filtradas a traves de una fecha especifica 
# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class PeticionFechaListView(generics.ListAPIView):
    serializer_class = PeticionSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener la fecha de la url
        fecha = self.kwargs['fecha']
        # Obtener el id del usuario
        id_usuario = self.kwargs['id']
        # Obtener el usuario del id
        usuario = UsuarioComun.objects.get(id=id_usuario)
        # Filtramos las peticiones por fecha y usuario
        peticiones = Peticion.objects.filter(fecha_registro_peticion=fecha, usuario_comun=usuario, estado_revision=True)
        return peticiones


##### Lista de peticiones filtradas a traves de un rango de días específico
# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class PeticionRangoListView(generics.ListAPIView):
    serializer_class = PeticionSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener el valor del rango de la url
        rango = self.kwargs['rango']
        # Obtener el id del usuario
        id_usuario = self.kwargs['id']
        # Obtener el usuario del id
        usuario = UsuarioComun.objects.get(id=id_usuario)
        # Filtramos las peticiones desde la fecha actual hasta el rango de dias y usuario
        peticiones = Peticion.objects.filter(fecha_registro_peticion__range=[datetime.now()-timedelta(days=rango), datetime.now()], usuario_comun=usuario, estado_revision=True)
        return peticiones


##### Lista de peticiones pendientes filtradas a través de una fecha específica
# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class PeticionFechaPendienteListView(generics.ListAPIView):
    serializer_class = PeticionSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener la fecha de la url
        fecha = self.kwargs['fecha']
        # Filtramos las peticiones por fecha y usuario
        peticiones = Peticion_Pendiente_Fecha(self.request, fecha)
        return peticiones

def Peticion_Pendiente_Fecha(ob1, ob2):
    try:
        # Decodifica el token para obtener el usuario que inicio sesion
        token = ob1.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        # Encontrar al usuario relacionado al user de tipo tecnico
        if is_tecnico(user):
            # Obtener las peticiones por tipo y que no han sido revisadas
            peticiones_fecha = Peticion.objects.filter(fecha_registro_peticion=ob2, estado_revision=False)
            return peticiones_fecha
        else:
            return []
    except Peticion.DoesNotExist:
        return []

##### Lista de peticiones pendientes filtradas a traves de un rango de días específico
# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class PeticionRangoPendienteListView(generics.ListAPIView):
    serializer_class = PeticionSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener el valor del rango de la url
        rango = self.kwargs['rango']
        # Filtramos las peticiones desde la fecha actual hasta el rango de dias y usuario
        peticiones = Peticion_Pendiente_Rango(self.request, rango)
        return peticiones


def Peticion_Pendiente_Rango(ob1, ob2):
    try:
        # Decodifica el token para obtener el usuario que inicio sesion
        token = ob1.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        # Encontrar al usuario relacionado al user de tipo tecnico
        if is_tecnico(user):
            # Obtener las peticiones por tipo y que no han sido revisadas
            peticiones_rango = Peticion.objects.filter(fecha_registro_peticion__range=[datetime.now()-timedelta(days=ob2), datetime.now()], estado_revision=False)
            return peticiones_rango
        else:
            return []
    except Peticion.DoesNotExist:
        return []


##### Lista de peticiones pendientes filtradas por una fecha específica 
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class PeticionFechaAtendidaListView(generics.ListAPIView):
    serializer_class = PeticionSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener la fecha de la url
        fecha = self.kwargs['fecha']
        # Filtramos las peticiones por fecha y usuario
        peticiones = Peticion.objects.filter(fecha_registro_peticion=fecha, estado_revision=True)
        return peticiones


##### Lista de peticiones atendidas filtradas a traves de un rango de días específico
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class PeticionRangoAtendidaListView(generics.ListAPIView):
    serializer_class = PeticionSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener el valor del rango de la url
        rango = self.kwargs['rango']
        # Filtramos las peticiones desde la fecha actual hasta el rango de dias y usuario
        peticiones = Peticion.objects.filter(fecha_registro_peticion__range=[datetime.now()-timedelta(days=rango), datetime.now()], estado_revision=True)
        return peticiones
    

##### Lista de reportes perteneciente a un usuario comun filtrado mediante el nombre
##### de un paciente en especifico
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ReportedePacienteListView(generics.ListAPIView):
    serializer_class = ReporteSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener nombre y apellido de la url
        nombre, apellido = self.kwargs['nombre'].split(' ', 1)
        if (nombre_paciente_exist(nombre , apellido)):
            # Filtrar registros de resultados por el nombre del paciente
            reportes = reporte_por_nombre(self.request, nombre, apellido)
            return reportes
        else:
            return []


def reporte_por_nombre(request, nombre, apellido):
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
                # Obtener los reportes  del paciente
                reportes = Reporte.objects.filter(paciente=paciente__ob).order_by('fecha_registro_reporte')
                return reportes
            else :
                return []
        else:
            if is_tecnico(user):
                # Obtener el paciente por nombre y apellido ignorando mayusculas y minusculas
                paciente__ob = Paciente.objects.get(nombre_usuario__icontains=nombre, apellido_usuario__icontains=apellido)
                # Obtener los reportes  del paciente
                reportes = Reporte.objects.filter(paciente=paciente__ob).order_by('fecha_registro_reporte')
                return reportes
            else:
                return []
    except UsuarioComun.DoesNotExist:
        return []
    except Paciente.DoesNotExist:
        return []
    except Curso.DoesNotExist:
        return []
    except Reporte.DoesNotExist:
        return []



##### Lista de salas filtradas a traves de una fecha específica y el usuario comun
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class SalaFechaListView(generics.ListAPIView):
    serializer_class = SalaSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener la fecha de la url
        fecha = self.kwargs['fecha']
        # Obtenemos el id de la url
        id_usuario = self.kwargs['id']
        # Llamamos al metodo
        salas = sala_por_fecha(id_usuario, fecha)
        return salas


def sala_por_fecha(ob1, ob2):
    try:
        # Obtener el usuario comun
        usuario__ob = UsuarioComun.objects.get(id=ob1)
        # Obtener el detalle de sala asociada al usuario comun
        detalles_sala_usuario = DetalleSala.objects.filter(usuario_comun=usuario__ob)
        # Obtener las salas asociadas al detalle de sala
        salas = Sala.objects.filter(detallesala__in=detalles_sala_usuario, fecha_registro_sala=ob2, sala_atendida=False)
        return salas
    except UsuarioComun.DoesNotExist:
        return []
    except DetalleSala.DoesNotExist:
        return []
    except Sala.DoesNotExist:
        return []
    

##### Lista de salas filtradas a traves de una fecha específica
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class SalaFechaTecnicoListView(generics.ListAPIView):
    serializer_class = SalaSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener la fecha de la url
        fecha = self.kwargs['fecha']
        # Listamos las salas en esa fecha
        salas = Sala.objects.filter(fecha_registro_sala=fecha).order_by('nombre_sala')
        return salas


##### Lista de salas atendidas filtradas a traves de una fecha específica y el usuario comun
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class SalaFechaAtendidaListView(generics.ListAPIView):
    serializer_class = SalaSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener la fecha de la url
        fecha = self.kwargs['fecha']
        # Obtenemos el id de la url
        id_usuario = self.kwargs['id']
        # Llamamos al metodo
        salas = sala_por_fecha_atendida(id_usuario, fecha)
        return salas


def sala_por_fecha_atendida(ob1, ob2):
    try:
        # Obtener el usuario comun
        usuario__ob = UsuarioComun.objects.get(id=ob1)
        # Obtener el detalle de sala asociada al usuario comun
        detalles_sala_usuario = DetalleSala.objects.filter(usuario_comun=usuario__ob)
        # Obtener las salas asociadas al detalle de sala
        salas = Sala.objects.filter(detallesala__in=detalles_sala_usuario, fecha_registro_sala=ob2, sala_atendida=True)
        return salas
    except UsuarioComun.DoesNotExist:
        return []
    except DetalleSala.DoesNotExist:
        return []
    except Sala.DoesNotExist:
        return []
    

##### Lista de salas filtradas por el usuario comun
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


##### Lista de salas atendidas filtradas por el usuario comun
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


##### Lista de cursos filtrados para el usuario comun
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


##### Lista de salas pertenecientes a un paciente específico
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


##### Lista de salas filtradas mediante el nombre de una sala
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


##### Busqueda de contenido mediante nombre e
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



##### Lista de cursos filtrados mediante el nombre de un curso
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


##### Lista de resultados filtrados 
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
    

##### Lista de cursos filtrados mediante una fecha específica
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CursoFechaListView(generics.ListAPIView):
    serializer_class = CursoSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener la fecha de la url
        fecha = self.kwargs['fecha']
        # Llamamos al metodo
        cursos_fecha = curso_por_fecha(self.request, fecha)
        return cursos_fecha


def curso_por_fecha(ob1, ob2):
    try:
        # Decodifica el token para obtener el usuario comun
        token = ob1.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        # Encontrar al usuario relacionado al user obtenido
        if is_comun(user):
            # Obtener el usuario comun
            usuario__ob = UsuarioComun.objects.get(user=user)
            # Obtener los cursos creados por el usuario comun y en la fecha de establecida
            cursos_fecha = Curso.objects.filter(usuario_comun=usuario__ob, fecha_registro_curso=ob2).order_by('nombre_curso')
            return cursos_fecha
        else:
            return []
    except UsuarioComun.DoesNotExist:
        return []
    except Curso.DoesNotExist:
        return []
    

##### Lista de cursos filtrados mediante una fecha especifica 
##### para el usuario tecnico sin una restricción adicional
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CursoFechaTecnicoListView(generics.ListAPIView):
    serializer_class = CursoSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener la fecha de la url
        fecha = self.kwargs['fecha']
        # Filtramos los cursos basados en la fecha
        cursos_fecha_tecnico = Curso.objects.filter(fecha_registro_curso=fecha).order_by('nombre_curso')
        return cursos_fecha_tecnico
    

###### Lista de resultados en base a una fecha especifica
###### Para visualización de un grupo de resultados especificos
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ResultadoFechaTecnicoListView(generics.ListAPIView):
    serializer_class = ResultadoSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener la fecha de la url
        fecha = self.kwargs['fecha']
        # Filtramos los resultados basados en la fecha
        resultado_fecha_tecnico = Resultado.objects.filter(fecha_registro_resultado=fecha).order_by('fecha_registro_resultado')
        return resultado_fecha_tecnico

###### Lista de resultados en base a una fecha especifica
###### Para visualización de un grupo de resultados especificos
###### Para el usuario comun. Se requiere filtrar por curso y paciente
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ResultadoFechaListView(generics.ListAPIView):
    serializer_class = ResultadoSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener la fecha de la url
        fecha = self.kwargs['fecha']
        # Filtramos los cursos basados en la fecha
        resultado_fecha = resultado_por_fecha(self.request, fecha)
        return resultado_fecha

def resultado_por_fecha(ob1, ob2):
    try:
        # Obtenemso el token del usuario comun
        token = ob1.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        # Encontrar al usuario relacionado al user obtenido
        if is_comun(user):
            # Obtener el usuario comun
            usuario__ob = UsuarioComun.objects.get(user=user)
            # Obtener los cursos creados por el usuario comun
            cursos = Curso.objects.filter(usuario_comun=usuario__ob)
            # Obtener los pacientes inscritos en esos cursos
            pacientes_inscritos_curso = Paciente.objects.filter(detalleinscripcioncurso__curso__in=cursos).distinct()
            # Obtener los resultados de esos pacientes
            resultados_obt = Resultado.objects.filter(paciente__in=pacientes_inscritos_curso, fecha_registro_resultado=ob2).order_by('fecha_registro_resultado')
            return resultados_obt
        else:
            return []
    except UsuarioComun.DoesNotExist:
        return []
    except Curso.DoesNotExist:
        return []
    except Paciente.DoesNotExist:
        return []
    except Resultado.DoesNotExist:
        return []


###### Lista de resultados en base a una rango de dias especifico
###### Para visualización de un grupo de resultados especificos
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ResultadoRangoTecnicoListView(generics.ListAPIView):
    serializer_class = ResultadoSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener el rango de la url
        rango = self.kwargs['rango']
        # Filtramos los resultados basados en un rango de dias
        resultado_rango_tecnico = Resultado.objects.filter(fecha_registro_resultado__range=[datetime.now()-timedelta(days=rango), datetime.now()]).order_by('fecha_registro_resultado')
        return resultado_rango_tecnico


###### Lista de resultados en base a una fecha especifica
###### Para visualización de un grupo de resultados especificos
###### Para el usuario comun. Se requiere filtrar por curso y paciente
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ResultadoRangoListView(generics.ListAPIView):
    serializer_class = ResultadoSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener la fecha de la url
        rango = self.kwargs['rango']
        # Filtramos los cursos basados en la fecha
        resultado_fecha = resultado_por_rango(self.request, rango)
        return resultado_fecha

def resultado_por_rango(ob1, ob2):
    try:
        # Obtenemso el token del usuario comun
        token = ob1.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        # Encontrar al usuario relacionado al user obtenido
        if is_comun(user):
            # Obtener el usuario comun
            usuario__ob = UsuarioComun.objects.get(user=user)
            # Obtener los cursos creados por el usuario comun
            cursos = Curso.objects.filter(usuario_comun=usuario__ob)
            # Obtener los pacientes inscritos en esos cursos
            pacientes_inscritos_curso = Paciente.objects.filter(detalleinscripcioncurso__curso__in=cursos).distinct()
            # Obtener los resultados de esos pacientes
            resultados_rango = Resultado.objects.filter(paciente__in=pacientes_inscritos_curso,
                                                      fecha_registro_resultado__range=[datetime.now()-timedelta(days=ob2), datetime.now()]).order_by('fecha_registro_resultado')
            return resultados_rango
        else:
            return []
    except UsuarioComun.DoesNotExist:
        return []
    except Curso.DoesNotExist:
        return []
    except Paciente.DoesNotExist:
        return []
    except Resultado.DoesNotExist:
        return []



###### Lista de reportes en base a una fecha especifica
###### Permite el filtrado de todos los reportes de un usuario comun en base 
###### a una fecha
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ReporteFechaTecnicoListView(generics.ListAPIView):
    serializer_class = ReporteSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener la fecha de la url
        fecha = self.kwargs['fecha']
        # Filtramos los resultados basados en la fecha
        reporte_fecha_tecnico = Reporte.objects.filter(fecha_registro_reporte=fecha).order_by('fecha_registro_reporte')
        return reporte_fecha_tecnico
    

###### Lista de reportes en base a una fecha especifica
###### Permite el filtrado de todos los reportes de un usuario comun en base 
###### a una fecha
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ReporteFechaListView(generics.ListAPIView):
    serializer_class = ReporteSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener la fecha de la url
        fecha = self.kwargs['fecha']
        # Filtramos los resultados basados en la fecha
        reporte_fecha_comun = reporte_por_fecha(self.request, fecha)
        return reporte_fecha_comun

def reporte_por_fecha(ob1, ob2):
    try:
        # Obtenemso el token del usuario comun
        token = ob1.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        # Encontrar al usuario relacionado al user obtenido
        if is_comun(user):
            # Obtener el usuario comun
            usuario__ob = UsuarioComun.objects.get(user=user)
            # Obtener los reportes creados por el usuario comun en una fecha especifica
            reportes_fecha = Reporte.objects.filter(usuario_comun=usuario__ob, fecha_registro_reporte=ob2).order_by('fecha_registro_reporte')
            return reportes_fecha
        else:
            return []
    except UsuarioComun.DoesNotExist:
        return []
    except Reporte.DoesNotExist:
        return []



###### Lista de reportes en base a un rango de dias
###### Permite el filtrado de todos los reportes de un usuario comun en base 
###### a un rango de dias limite
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ReporteRangoTecnicoListView(generics.ListAPIView):
    serializer_class = ReporteSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener la fecha de la url
        rango = self.kwargs['rango']
        # Filtramos los resultados basados en un rango de dias 
        reporte_rango_tecnico = Reporte.objects.filter(fecha_registro_reporte__range=[datetime.now()-timedelta(days=rango), datetime.now()]).order_by('fecha_registro_reporte')
        return reporte_rango_tecnico


###### Lista de reportes en base a una fecha especifica
###### Permite el filtrado de todos los reportes de un usuario comun en base 
###### a una fecha
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ReporteRangoListView(generics.ListAPIView):
    serializer_class = ReporteSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener la fecha de la url
        rango = self.kwargs['rango']
        # Filtramos los resultados basados en el rango de dias
        reporte_rango_comun = reporte_por_rango(self.request, rango)
        return reporte_rango_comun

def reporte_por_rango(ob1, ob2):
    try:
        # Obtenemso el token del usuario comun
        token = ob1.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        # Encontrar al usuario relacionado al user obtenido
        if is_comun(user):
            # Obtener el usuario comun
            usuario__ob = UsuarioComun.objects.get(user=user)
            # Obtener los reportes creados por el usuario comun en un limite de dias
            reportes_fecha = Reporte.objects.filter(usuario_comun=usuario__ob, 
                                                    fecha_registro_reporte__range=[datetime.now()-timedelta(days=ob2), datetime.now()]).order_by('fecha_registro_reporte')
            return reportes_fecha
        else:
            return []
    except UsuarioComun.DoesNotExist:
        return []
    except Reporte.DoesNotExist:
        return []


###### Lista de reportes en base a un número de cédula
###### Permite el filtrado de todos los reportes de un usuario comun o técnico en base 
###### a una cédula d estudiante
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ReporteCedulaListView(generics.ListAPIView):
    serializer_class = ReporteSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener la fecha de la url
        cedula_ = self.kwargs['cedula']
        # Filtramos los resultados basados en la fecha
        if not Paciente_Existe_Cedula(cedula_):
            return []
        # Filtramos los reportes basados en la cedula del Estudiante
        reporte_cedula_comun = Reporte_por_Cedula(self.request, cedula_)
        return reporte_cedula_comun

def Reporte_por_Cedula(ob1, ob2):
    try:
        # Obtenemso el token del usuario comun
        token = ob1.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        # Encontrar al usuario relacionado al user obtenido
        if is_comun(user):
            # Obtener el usuario comun
            usuario__ob = UsuarioComun.objects.get(user=user)
            # Obtener los resultados asociados al paciente mediante el dni
            resultados= Resultado.objects.filter(paciente__dni=ob2)
            # Obtener los reportes creados por el usuario comun y que esten dentro de 
            # de los resultados obtenidos
            reportes_cedula = Reporte.objects.filter(usuario_comun=usuario__ob, resultado__in=resultados).order_by('fecha_registro_reporte')
            return reportes_cedula
        elif is_tecnico(user):
            # Obtener los resultados asociados al paciente mediante el dni
            resultados= Resultado.objects.filter(paciente__dni=ob2)
            # Obtener los reportes creados y que esten dentro de 
            # de los resultados obtenidos
            reportes_cedula = Reporte.objects.filter(resultado__in=resultados).order_by('fecha_registro_reporte')
            return reportes_cedula
        else:
            return []
    except UsuarioComun.DoesNotExist:
        return []
    except Reporte.DoesNotExist:
        return []
    
def Paciente_Existe_Cedula(ob1):
    try:
        if Paciente.objects.filter(dni=ob1).exists():
            return True
        return False
    except Paciente.DoesNotExist:
        return False
    


###### Lista de reportes en base a un número de cédula
###### Permite el filtrado de todos los reportes de un usuario comun o técnico en base 
###### a una cédula d estudiante
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ResultadoCedulaListView(generics.ListAPIView):
    serializer_class = ResultadoSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener la fecha de la url
        cedula_ = self.kwargs['cedula']
        # Filtramos los resultados basados en la fecha
        if not Paciente_Existe_Cedula(cedula_):
            return []
        # Filtramos los reportes basados en la cedula del Estudiante
        resultado_cedula_comun = Resultado_por_Cedula(self.request, cedula_)
        return resultado_cedula_comun

def Resultado_por_Cedula(ob1, ob2):
    try:
        # Obtenemso el token del usuario comun
        token = ob1.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        # Encontrar al usuario relacionado al user obtenido
        if is_comun(user):
            # Obtener el usuario comun a traves del user
            usuario__ob = UsuarioComun.objects.get(user=user)
            # Obtener la lista de los cursos creados por el usuario comun
            cursos_crea = Curso.objects.filter(usuario_comun=usuario__ob)
            # Obtener la lista de los pacientes inscritos en esos cursos
            pacientes_inscritos_curso = Paciente.objects.filter(detalleinscripcioncurso__curso__in=cursos_crea).distinct()
            # Obtener el paciente asociada a esa cédula
            ob_paciente = Paciente.objects.get(dni=ob2)
            # Obtener los resultados de ese paciente con ese numero de cédula
            resultados_cedula = Resultado.objects.filter(paciente=ob_paciente, paciente__in=pacientes_inscritos_curso).order_by('fecha_registro_resultado')
            return resultados_cedula
        elif is_tecnico(user):
            # Obtener los reportes creados por el usuario comun y que pertenezcan a un paciente especifico 
            # por medio de la céula
            resultados_cedula = Resultado.objects.filter(paciente__dni=ob2).order_by('fecha_registro_resultado')
            return resultados_cedula
        else:
            return []
    except UsuarioComun.DoesNotExist:
        return []
    except Curso.DoesNotExist:
        return []
    except Paciente.DoesNotExist:
        return []
    except Resultado.DoesNotExist:
        return []


###### Obtención del registro de estudiante por medio de la cédula
###### Permite el filtrado el registro de un estudiante por medio de su cédula
###### siempre y cuando pertenezca a un curso especifico por medio de su slug de curso
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class EstudianteCedulaListView(generics.ListAPIView):
    serializer_class = PacienteSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener la fecha de la url
        cedula_ = self.kwargs['cedula']
        slug_ = self.kwargs['slug']
        # Filtramos la existencia del paciente basados en la cédula
        if not Paciente_Existe_Cedula(cedula_):
            return []
        # Filtramos los reportes basados en la cedula del Estudiante
        estudiante_cedula_comun = Estudiante_por_Cedula(self.request, cedula_, slug_)
        return estudiante_cedula_comun


def Estudiante_por_Cedula(ob1, ob2, ob3):
    try:
        # Obtenemso el token del usuario comun
        token = ob1.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        # Encontrar al usuario relacionado al user obtenido
        if is_comun(user):
            # Obtener el usuario comun a traves del user
            usuario__ob = UsuarioComun.objects.get(user=user)
            # Obtener la lista de los cursos creados por el usuario comun
            cursos_creados = Curso.objects.filter(usuario_comun=usuario__ob)
            # Obtener el curso asociado al slug
            curso_especifico = Curso.objects.get(slug_curso=ob3)
            # Obtener la lista de los pacientes inscritos en ese curso
            pacientes_inscritos = Paciente.objects.filter(detalleinscripcioncurso__curso__in=cursos_creados, detalleinscripcioncurso__curso=curso_especifico).distinct()
            # Devolvemos el registro de paciente asociado a esa cédula dentro de la lista de pacientes dentro del curso
            return pacientes_inscritos.filter(dni=ob2)
        else:
            return []
    except UsuarioComun.DoesNotExist:
        return []
    except Curso.DoesNotExist:
        return []
    except Paciente.DoesNotExist:
        return []


###### Obtención de los registros de reportes generados por un usuario comun asociados
###### a un estudiante a travs de sus nombre y apellidos. Se considera que el estudiante
###### debe ser buscado por sus dos nombres y apellidos completos debido a problemas
###### de nombre o incluso apellidos similares: casos familiares
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class EstudianteNomApeListView(generics.ListAPIView):
    serializer_class = ReporteSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener los nombres y apellidosde la url
        nombres_completos = self.kwargs['nombre']
        # Dividir los nombres y apellidos en una lista
        nombres_apellidos = nombres_completos.split()
        # Controlar que nombres_apellidos tenga 4 o 5 elementos
        if len(nombres_apellidos) not in [4, 5]:
            return []
        # Obtener el nombre y apellido
        nombre = ' '.join(nombres_apellidos[:3] if len(nombres_apellidos) == 5 else nombres_apellidos[:2])
        apellido = ' '.join(nombres_apellidos[3:] if len(nombres_apellidos) == 5 else nombres_apellidos[2:])
        # Controlar valides de entrada
        if not validar_nombres(nombre, apellido):
            return []
        # Validar existencia de cedula
        if not Obtener_Cedula(nombre, apellido):
            return []
        cedula_paciente = Obtener_Cedula(nombre, apellido)
        # Filtramos la existencia del estudiante basados en la cédula
        if not Paciente_Existe_Cedula(cedula_paciente):
            return []
        # Filtramos
        reportes = Reporte_por_Nombre_Apellido(self.request, nombre, apellido)
        return reportes

#### Método para obtener la cedula de un estudiante
def Obtener_Cedula(ob1, ob2):
    try:
        cedula_paciente = Paciente.objects.get(nombre_usuario__iexact=ob1, apellido_usuario__iexact=ob2).dni
        return cedula_paciente
    except Paciente.DoesNotExist:
        return []

#### Filtrar los reportes por nombres y apellidos del estudiante
def Reporte_por_Nombre_Apellido(request, nombre, apellido):
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
                resultados = Resultado.objects.filter(paciente=paciente__ob)
                # Obtener los reportes  del paciente acorde a los resultados
                reportes = Reporte.objects.filter(resultado__in=resultados).order_by('fecha_registro_reporte')
                return reportes
            else :
                return []
        else:
            if is_tecnico(user):
                # Obtener el paciente por nombre y apellido ignorando mayusculas y minusculas
                paciente__ob = Paciente.objects.get(nombre_usuario__icontains=nombre, apellido_usuario__icontains=apellido)
                # Obtener los resultados del paciente
                resultados = Resultado.objects.filter(paciente=paciente__ob)
                # Obtener los reportes  del paciente
                reportes = Reporte.objects.filter(resultado__in=resultados).order_by('fecha_registro_reporte')
                return reportes
            else:
                return []
    except UsuarioComun.DoesNotExist:
        return []
    except Paciente.DoesNotExist:
        return []
    except Curso.DoesNotExist:
        return []
    except Reporte.DoesNotExist:
        return []



###### Obtención de los registros de resultados generados por un estudiante asociados
###### a un uuario comun a travs de sus nombre y apellidos. Se considera que el estudiante
###### debe ser buscado por sus dos nombres y apellidos completos debido a problemas
###### de nombre o incluso apellidos similares: casos familiares y obtener la cedula para
###### ser filtrado por medio de ella|
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ResultadoNomApeListView(generics.ListAPIView):
    serializer_class = ResultadoSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener los nombres y apellidosde la url
        nombres_completos = self.kwargs['nombre']
        # Dividir los nombres y apellidos en una lista
        nombres_apellidos = nombres_completos.split()
        # Controlar que nombres_apellidos tenga 4 o 5 elementos
        if len(nombres_apellidos) not in [4, 5]:
            return []
        # Obtener el nombre y apellido
        nombre = ' '.join(nombres_apellidos[:3] if len(nombres_apellidos) == 5 else nombres_apellidos[:2])
        apellido = ' '.join(nombres_apellidos[3:] if len(nombres_apellidos) == 5 else nombres_apellidos[2:])
        # Controlar valides de entrada
        if not validar_nombres(nombre, apellido):
            return []
        # Validar existencia de cedula
        if not Obtener_Cedula(nombre, apellido):
            return []
        cedula_paciente = Obtener_Cedula(nombre, apellido)
        # Filtramos la existencia del estudiante basados en la cédula
        if not Paciente_Existe_Cedula(cedula_paciente):
            return []
        # Filtramos
        resultados = Resultado_por_Cedula(self.request, cedula_paciente)
        return resultados


###### Obtención de los registros de estudiante inscritos a un curso asociado
###### a un uuario comun; a traves de sus nombre y apellidos del estudiante. Se considera que el estudiante
###### debe ser buscado por sus dos nombres y apellidos completos debido a problemas
###### de nombre o incluso apellidos similares: casos familiares. Y con ello obtener la cedula para
###### ser filtrado por medio de ella|
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class BusquedaPacienteCursoListView(generics.ListAPIView):
    serializer_class = PacienteSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener los nombres y apellidosde la url
        slug_ = self.kwargs['slug']
        nombres_completos = self.kwargs['nombre']
        # Dividir los nombres y apellidos en una lista
        nombres_apellidos = nombres_completos.split()
        # Controlar que nombres_apellidos tenga 4 o 5 elementos
        if len(nombres_apellidos) not in [4, 5]:
            return []
        # Obtener nombres y apellidos
        nombre = ' '.join(nombres_apellidos[:3] if len(nombres_apellidos) == 5 else nombres_apellidos[:2])
        apellido = ' '.join(nombres_apellidos[3:] if len(nombres_apellidos) == 5 else nombres_apellidos[2:])
        # Controlar valides de entrada
        if not validar_nombres(nombre, apellido):
            return []
        # Validar existencia de cedula
        if not Obtener_Cedula(nombre, apellido):
            return []
        # Obtener cédula
        cedula_paciente = Obtener_Cedula(nombre, apellido)
        # Filtramos la existencia del estudiante basados en la cédula
        if not Paciente_Existe_Cedula(cedula_paciente):
            return []
        # Filtramos
        registro_estudiante = Estudiante_por_Cedula(self.request, cedula_paciente, slug_)
        return registro_estudiante
        
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



#### Permite obtener la lista de peticiones que existe por medio del tipo y que su estado de revision sea falso
### la busqueda es general ya que pertenece al usuario tecnico
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class PeticionTipoPendienteListView(generics.ListAPIView):
    serializer_class = PeticionSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener el valor del rango de la url
        tipo = self.kwargs['tipo']
        # Filtramos las peticiones desde la fecha actual hasta el rango de dias y usuario
        peticiones_tipo = Peticion_por_Tipo(self.request, tipo)
        return peticiones_tipo

### Busqueda de las peticiones pendiante por medio del tipo de petición
def Peticion_por_Tipo(ob1, ob2):
    try:
        # Decodifica el token para obtener el usuario
        token = ob1.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        # Encontrar al usuario relacionado al user de tipo tecnico
        if is_tecnico(user):
            # Obtener las peticiones por tipo y que no han sido revisadas
            peticiones_tipo = Peticion.objects.filter(tipo_peticion=ob2, estado_revision=False)
            return peticiones_tipo
        else:
            return []
    except Peticion.DoesNotExist:
        return []



#### Permite obtener la lista de peticiones que existe por medio del tipo y que su estado de revision sea true
### la busqueda es general ya que pertenece al usuario tecnico
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class PeticionTipoPendienteListViewAA(generics.ListAPIView):
    serializer_class = PeticionSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener el valor del rango de la url
        tipo = self.kwargs['tipo']
        # Filtramos las peticiones desde la fecha actual hasta el rango de dias y usuario
        peticiones_tipo = Peticion_por_Tipo_Aten(self.request, tipo)
        return peticiones_tipo

## Busqueda de las peticiones pendiante por medio del tipo de petición
def Peticion_por_Tipo_Aten(ob1, ob2):
    try:
        # Decodifica el token para obtener el usuario
        token = ob1.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        # Encontrar al usuario relacionado al user de tipo tecnico
        if is_tecnico(user):
            # Obtener las peticiones por tipo y que no han sido revisadas
            peticiones_tipo_a = Peticion.objects.filter(tipo_peticion=ob2, estado_revision=True)
            return peticiones_tipo_a
        else:
            return []
    except Peticion.DoesNotExist:
        return []


##### Lista de peticiones filtradas a traves de un rango de días específico
# PROTECCION CON JWT
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class PeticionTipo_U_ListView(generics.ListAPIView):
    serializer_class = PeticionSerializer
    pagination_class = Paginacion
    def get_queryset(self):
        # Obtener el valor del rango de la url
        tipo = self.kwargs['tipo']
        # Obtener el id del usuario
        id_usuario = self.kwargs['id']
        # Filtramos las peticiones desde la fecha actual hasta el rango de dias y usuario
        peticiones = Peticion_Usuario_tipo(id_usuario, tipo)
        return peticiones

def Peticion_Usuario_tipo(ob1, ob2):
    try:
        # Obtener el usuario comun
        usuario = UsuarioComun.objects.get(id=ob1)
        # Obtener las peticiones por tipo y que no han sido revisadas
        peticiones_tipo = Peticion.objects.filter(tipo_peticion=ob2, usuario_comun=usuario, estado_revision=True)
        return peticiones_tipo
    except UsuarioComun.DoesNotExist:
        return []
    except Peticion.DoesNotExist:
        return []