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
                  'username_usuario', 'celular', 'fecha_nacimiento', 'user')


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ( 'id', 'nombre_usuario', 'apellido_usuario', 'email_usuario', 'username_usuario',
                  'celular', 'contacto_emergencia', 'fecha_nacimiento', 'direccion', 'edad', 'user')


class ComunSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioComun
        fields = ('nombre_usuario', 'apellido_usuario', 'email_usuario', 'username_usuario',
                  'celular', 'genero', 'fecha_nacimiento', 'area_estudio', 'edad', 'user')


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
                  'portada_individual', 'nivel', 'tipo_contenido', 'contenido_individual', 'contenido')


class ResultadoSerializer(serializers.ModelSerializer):
    nombre_paciente = serializers.SerializerMethodField()
    apellido_paciente = serializers.SerializerMethodField()

    class Meta:
        model = Resultado
        fields = ('id', 'respuesta', 'tiempo_m', 'tiempo_s', 'observacion', 'fecha_registro_resultado',
                  'slug_resultado', 'estado_resultado', 'contenido_individual', 'paciente',
                  'nombre_paciente', 'apellido_paciente')
    def get_nombre_paciente(self, obj):
        return obj.paciente.nombre_usuario
    def get_apellido_paciente(self, obj):
        return obj.paciente.apellido_usuario

class ResultadoSerializerOnly(serializers.ModelSerializer):
    class Meta:
        model = Resultado
        fields = ('id', 'observacion')

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ('id', 'nombre_curso', 'descripcion_curso', 'slug_curso', 'usuario_comun',
                  'identificador_curso')


class DetalleInscripcionCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleInscripcionCurso
        fields = ('id', 'fecha_inscripcion',
                  'estado_detalle', 'paciente', 'curso')


class PeticionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peticion
        fields = ('id', 'motivo_peticion', 'tipo_peticion', 'slug_peticion',
                  'estado_revision', 'peticion_cuerpo', 'usuario_comun')

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
                  'sala_atendida', 'paciente')

class DetalleSalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleSala
        fields = ('id', 'fecha_detalle_sala', 'estado_detalle_sala', 'sala', 'usuario_comun')

class ReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte
        fields = ('id', 'titulo_reporte', 'descripcion_reporte', 'slug_reporte', 'estado_reporte', 
                  'usuario_comun', 'contenido')