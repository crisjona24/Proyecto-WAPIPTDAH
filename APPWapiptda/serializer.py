from .models import *
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('nombre_usuario', 'apellido_usuario', 'email_usuario',
                  'username_usuario', 'celular', 'fecha_nacimiento', 'is_activo', 'user')


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ( 'id', 'nombre_usuario', 'apellido_usuario', 'email_usuario', 'username_usuario',
                  'celular', 'contacto_emergencia', 'fecha_nacimiento', 'direccion', 'edad', 'is_activo', 'user')


class ComunSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioComun
        fields = ('nombre_usuario', 'apellido_usuario', 'email_usuario', 'username_usuario',
                  'celular', 'genero', 'fecha_nacimiento', 'area_estudio', 'edad', 'is_activo', 'user')


class GraditoTDAHSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradoTDAH
        fields = ('id', 'nombre_nivel', 'descripcion_grado', 'numero_categorias', 'grado_dificultad',
                  'slug_grado', 'usuario_tecnico')


class DominioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dominio
        fields = ('id', 'nombre', 'descripcion', 'slug_dominio',
                  'identificador_dominio', 'portada_dominio')


class ContenidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contenido
        fields = ('id', 'nombre', 'identificador_contenido', 'slug_contenido',
                  'dominio_tipo', 'portada', 'dominio')


class ContenidIndividualSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContenidoIndividual
        fields = ('id', 'descripcion_individual', 'respuesta', 'identificador_individual', 'slug_contenido_individual',
                  'portada_individual', 'nivel', 'tipo_contenido', 'contenido_individual', 'imagen1', 'contenido',
                  'imagen2', 'imagen3')


class ResultadoSerializer(serializers.ModelSerializer):
    # Paciente
    nombre_paciente = serializers.SerializerMethodField()
    apellido_paciente = serializers.SerializerMethodField()
    correo_paciente = serializers.SerializerMethodField()
    celular_paciente = serializers.SerializerMethodField()
    edad_paciente = serializers.SerializerMethodField()
    # Actividad
    descripcion_individual = serializers.SerializerMethodField()
    respuesta_contenido = serializers.SerializerMethodField()
    tipo_contenido = serializers.SerializerMethodField()

    class Meta:
        model = Resultado
        fields = ('id', 'respuesta', 'tiempo_m', 'tiempo_s', 'observacion', 'fecha_registro_resultado',
                  'slug_resultado', 'estado_resultado', 'estado_reporte', 'contenido_individual', 'paciente',
                  'nombre_paciente', 'apellido_paciente', 'correo_paciente', 'celular_paciente', 'edad_paciente',
                  'tipo_contenido', 'descripcion_individual', 'respuesta_contenido')
        
    def get_nombre_paciente(self, obj):
        return obj.paciente.nombre_usuario
    def get_apellido_paciente(self, obj):
        return obj.paciente.apellido_usuario
    def get_correo_paciente(self, obj):
        return obj.paciente.email_usuario
    def get_edad_paciente(self, obj):
        return obj.paciente.edad
    def get_celular_paciente(self, obj):
        return obj.paciente.celular
    def get_descripcion_individual(self, obj):
        return obj.contenido_individual.descripcion_individual
    def get_respuesta_contenido(self, obj):
        return obj.contenido_individual.respuesta
    def get_tipo_contenido(self, obj):
        return obj.contenido_individual.tipo_contenido


class ResultadoSerializerOnly(serializers.ModelSerializer):
    class Meta:
        model = Resultado
        fields = ('id', 'observacion')


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ('id', 'nombre_curso', 'descripcion_curso', 'slug_curso', 'usuario_comun',
                  'identificador_curso', 'fecha_registro_curso')


class DetalleInscripcionCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleInscripcionCurso
        fields = ('id', 'fecha_inscripcion',
                  'estado_detalle', 'paciente', 'curso')


class PeticionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peticion
        fields = ('id', 'motivo_peticion', 'tipo_peticion', 'slug_peticion',
                  'estado_revision', 'peticion_cuerpo', 'fecha_registro_peticion', 'usuario_comun')


class DetallePeticionSerializer(serializers.ModelSerializer):
    #usuario_tecnico = serializers.SerializerMethodField()
    usuario_tecnico = serializers.CharField(source='usuario_tecnico.nombre_usuario', read_only=True)

    class Meta:
        model = DetallePeticion
        fields = ('id', 'motivo_peticion', 'fecha_detalle_peticion', 'estado_detalle_revision',
                  'peticion', 'usuario_tecnico')
        

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ('id', 'nombre_sala', 'anotaciones', 'codigo_identificador', 'slug_sala', 'estado_sala', 
                  'sala_atendida', 'fecha_registro_sala', 'paciente')


class DetalleSalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleSala
        fields = ('id', 'fecha_detalle_sala', 'estado_detalle_sala', 'sala', 'usuario_comun')


class ReporteSerializer(serializers.ModelSerializer):
    # Datos de paciente
    nombre_paciente = serializers.SerializerMethodField()
    apellido_paciente = serializers.SerializerMethodField()
    correo_paciente = serializers.SerializerMethodField()
    celular_paciente = serializers.SerializerMethodField()
    edad_paciente = serializers.SerializerMethodField()
    direccion_paciente = serializers.SerializerMethodField()
    # Datos de contenido individual
    descripcion_individual = serializers.SerializerMethodField()
    respuesta = serializers.SerializerMethodField()
    tipo_contenido = serializers.SerializerMethodField()
    identificador_contenido = serializers.SerializerMethodField()
    # Datos Resultado
    tiempo_m_ = serializers.SerializerMethodField()
    tiempo_s_ = serializers.SerializerMethodField()
    observacion_ = serializers.SerializerMethodField()
    fecha_registro_resultado_ = serializers.SerializerMethodField()

    class Meta:
        model = Reporte
        fields = ('id', 'titulo_reporte', 'descripcion_reporte', 'slug_reporte', 'estado_reporte', 
                  'usuario_comun', 'contenido_individual', 'paciente', 'resultado', 'fecha_registro_reporte',
                  'nombre_paciente', 'apellido_paciente', 'correo_paciente', 'descripcion_individual',
                  'respuesta', 'tipo_contenido', 'tiempo_m_', 'tiempo_s_', 'observacion_', 'celular_paciente',
                  'fecha_registro_resultado_', 'edad_paciente', 'direccion_paciente', 'identificador_contenido')
    
    def get_nombre_paciente(self, obj):
        return obj.paciente.nombre_usuario
    def get_apellido_paciente(self, obj):
        return obj.paciente.apellido_usuario
    def get_correo_paciente(self, obj):
        return obj.paciente.email_usuario
    def get_edad_paciente(self, obj):
        return obj.paciente.edad
    def get_celular_paciente(self, obj):
        return obj.paciente.celular
    def get_direccion_paciente(self, obj):
        return obj.paciente.direccion
    def get_descripcion_individual(self, obj):
        return obj.contenido_individual.descripcion_individual
    def get_respuesta(self, obj):
        return obj.contenido_individual.respuesta
    def get_tipo_contenido(self, obj):
        return obj.contenido_individual.tipo_contenido
    def get_identificador_contenido(self, obj):
        return obj.contenido_individual.identificador_individual
    def get_tiempo_m_(self, obj):
        return obj.resultado.tiempo_m
    def get_tiempo_s_(self, obj):
        return obj.resultado.tiempo_s
    def get_observacion_(self, obj):
        return obj.resultado.observacion
    def get_fecha_registro_resultado_(self, obj):
        return obj.resultado.fecha_registro_resultado
    