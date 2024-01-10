from django.urls import path, include
from rest_framework import routers
from .views import *
from .controlers import *

# ROUTERS
router = routers.DefaultRouter()
router.register('user', UserView, basename='user')
router.register('usuario', UsuarioView)
router.register('paciente', PacienteView)
router.register('comun', ComunView, basename='comun')
# Movimiento a la otra app
router.register('grado', GradoTDAHView, basename='grado')
router.register('dominio', DominioView)
router.register('contenido', ContenidoView)
router.register('contenido_individual', ContenidoIndividualView)
router.register('resultado', ResultadoView, basename='resultado')
router.register('resultado/solo/', ResultadoViewOnly)
router.register('curso', CursoView)
router.register('detalle_inscripcion', DetalleInscripcionCursoView)
router.register('peticion', PeticionView)
router.register('detalle_peticion', DetallePeticionView)
router.register('sala', SalaView)
router.register('detalle_sala', DetalleSalaView)
router.register('reporte', ReporteView, basename='reporte')
router.register('dominios', ListaSoloDominiosView)
router.register('contenidos', ListaSoloContenidosView)

urlpatterns = [
    path('aplicacion/', include(router.urls)),
    # Token
    path('reenvio/codigo/cuenta/', reenvio_correo_verificacion, name='reverificar-cuenta'),
    path('verificar/cuenta/', verificar_email_firmado, name='verificar-cuenta'),
    path('cambiar/clave/', recuperar_cuenta, name='cambiar-clave'),
    path('verificar/codigo/cuenta/', verificar_email_recuperacion, name='nueva-clave'),
    path('registro/nueva/clave/', restablecer_clave, name='verificar-email-recuperacion'),

    ### LISTADOS PERSONALIZADOS ###
    
    ### REGISTRO ###

    path('registro_usuario/', api_user_register, name='api_user_register'),
    ############ Registro de estudiantes
    path('registro_paciente/', api_paciente_register, name='api_paciente_register'),
    ############ Registro de usuario comun
    path('registro_comun/', api_comun_register, name='api_comun_register'),
    
    ### CONTACTO ###

    ############ Envio de correo de contacto
    path('contacto/', api_enviar_contacto, name='enviar-contacto'),

    ### OBTENER DATOS ###

    ########### Obtención de datos de usuario
    path('datos/usuario/', datos_usuario, name='datos_usuario'),
    ########### Verificaciones
    path('verificar/usuario/', verificar_usuario, name='verificar_usuario'),
    ########### Obtención de slug
    path('obtener/curso/<int:id>/', obtener_slug_curso, name='obtener-slug-curso'),
    path('obtener/dominio/<str:slug>/', obtener_slug_dominio, name='obtener-slug-dominio'),
    path('obtener/contenido/<str:slug>/', obtener_slug_contenido, name='obtener-slug-contenido'),
    path('obtener/fecha/inscripcion/<int:id>/', obtener_fecha_inscripcion, name='obtener-fecha-inscripcion'),

    ### VERIFICACIONES ###
    path('verificar/inscripcion/', verificacion_inscripcion, name='verificar-inscripcion'),
    path('atender/peticion/', atender_peticion, name='atender-peticion'),
    path('atender/sala/<str:slug>/', atender_sala, name='atender-sala'),
    path('obtener/revisor/<int:id>/', obtener_nombre_revision, name='obtener-revisor'),

    ## NOTIFICACIONES ###
    path('contador/peticion/', get_contador_peticiones, name='contador-peticion'),
    path('contador/peticion/reinicio/', reset_contador_peticiones, name='reinicio-peticion'),
    path('contador/peticion/atendida/', get_contador_peticiones_atendidas, name='contador-peticion-atendida'),
    path('contador/atendido/reinicio/', reset_contador_peticiones_atendidas, name='reinicio-peticion-atendida'),
    path('contador/sala/', get_contador_salas, name='contador-sala'),
    path('contador/sala/reinicio/', reset_contador_salas, name='reinicio-sala'),
    path('contador/sala/atendida/', get_contador_salas_atendidas, name='contador-sala-atendida'),
    path('contador/sala/atendida/reinicio/', reset_contador_salas_atendidas, name='reinicio-sala-atendida'),
    path('modificar/estado/resultado/<int:id>/', modificar_estado_reporte, name='modificar-estado-resultado'),
]
