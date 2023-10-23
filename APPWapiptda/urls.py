from django.urls import path, include
from rest_framework import routers
from .views import *
from .controlers import *

# ROUTERS
router = routers.DefaultRouter()
router.register('user', UserView)
router.register('usuario', UsuarioView)
router.register('paciente', PacienteView)
router.register('comun', ComunView)
router.register('grado', GradoTDAHView)
router.register('dominio', DominioView)
router.register('contenido', ContenidoView)
router.register('contenido_individual', ContenidoIndividualView)
router.register('resultado', ResultadoView)
router.register('resultado/solo/', ResultadoViewOnly)
router.register('curso', CursoView)
router.register('detalle_inscripcion', DetalleInscripcionCursoView)
router.register('peticion', PeticionView)
router.register('detalle_peticion', DetallePeticionView)
router.register('sala', SalaView)
router.register('detalle_sala', DetalleSalaView)
router.register('reporte', ReporteView)
router.register('dominios', ListaSoloDominiosView)
router.register('contenidos', ListaSoloContenidosView)
#router.register('peticion/pendiente/', PeticionListViewNo)
#router.register('peticion/atendida/', PeticionListViewSi)

urlpatterns = [
    path('aplicacion/', include(router.urls)),
    # Token
    path('verificar/cuenta/', verificar_email_firmado, name='verificar-cuenta'),
    ### LISTADOS PERSONALIZADOS ###
    path('contenidos/<str:slug>/', ContenidoListView.as_view(), name='contenidos-list'),
    path('contenidos/individuales/<str:slug>/', ContenidoIndividualListView.as_view(), name='contenidos-individuales-list'),
    path('contenidos/individuales/nombre/<str:slug>/<str:nombre>/', CoInNombreListView.as_view(), name='contenidos-individuales-nombre-list'),
    path('peticion/pendiente/', PeticionListViewNo.as_view(), name='peticion-list-no'),
    path('peticion/atendida/', PeticionListViewSi.as_view(), name='peticion-list-si'),
    path('peticion/usuario/<int:id>/', PeticionUCListView.as_view(), name='peticion-list-usuario'),
    path('lista/pacientes/<int:id>/', PacientesListView.as_view(), name='peticion-list-usuario'),
    path('lista/resultados/<str:nombre>/', ResultadodePacienteListView2.as_view(), name='resultado-list-paciente'),
    path('lista/salas/<int:id>/', SalasListView.as_view(), name='sala-list-usuario'),
    path('lista/salas/atendidas/<int:id>/', SalasAtendidasListView.as_view(), name='sala-list-atendidas'),
    path('lista/salas/paciente/<int:id>/', SalasPacienteListView.as_view(), name='sala-list-paciente'),
    path('busqueda/salas/<str:nombre>/', BusquedaSalasListView.as_view(), name='salas-busqueda'),
    path('lista/cursos/', CursosListView.as_view(), name='cursos-list'),
    path('lista/resultado/usuario/<int:id>/', ResultadoListaUsuario.as_view(), name='resultado-list-usuario'),
    path('lista/reporte/usuario/<int:id>/', ListaReporteUsuarioComun.as_view(), name='reporte-list'),
    path('busqueda/paciente/curso/<str:nombre>/<str:slug>/', BusquedaPacienteCursoListView.as_view(), name='paciente-curso-busqueda'),
    path('busqueda/contenido/<str:nombre>/<str:slug>/', BusquedaContenidoListView.as_view(), name='contenido-busqueda'),
    path('busqueda/curso/<str:nombre>/', BusquedaCursoListView.as_view(), name='curso-busqueda'),
    path('lista/reportes/<str:nombre>/', ReportedePacienteListView.as_view(), name='reporte-list-paciente'),

    ### REGISTRO ###
    path('registro_usuario/', api_user_register, name='api_user_register'),
    path('registro_paciente/', api_paciente_register, name='api_paciente_register'),
    path('registro_comun/', api_comun_register, name='api_comun_register'),
    path('registro_contenido/', api_contenido_register, name='api_contenido_register'),
    path('registro_nivel/', api_nivel_register, name='api_nivel_register'),
    path('registro_dominio/', api_dominio_register, name='api_dominio_register'),
    path('registro_contenido_individual/', api_contenido_individual_register, name='registro_individual'),
    path('registro_curso/', api_curso_register, name='curso-registro'),
    path('registro/curso/<int:id>/', api_curso_inscripcion, name='inscripcion-registro'),
    path('registro_peticion/', api_peticion_register, name='peticion-registro'),
    path('registro_resultado/', save_resultado, name='registro-resultado'),
    path('registro_sala/', api_sala_register, name='registro-sala'),
    path('contacto/', api_enviar_contacto, name='enviar-contacto'),
    path('registro/reporte/<int:id>/', generar_reporte_resultado, name='registro-reporte'),

    ### OBTENER DATOS ###
    path('datos/usuario/', datos_usuario, name='datos_usuario'),
    path('verificar/usuario/', verificar_usuario, name='verificar_usuario'),
    path('verificar/nivel/<str:slug>/', verificar_nivel, name='verificar_nivel'),
    path('verificar/dominio/<str:slug>/', verificar_dominio, name='verificar_dominio'),
    path('verificar/contenido/<str:slug>/', verificar_contenido, name='verificar_contenido'),
    path('verificar/curso/<str:slug>/', verificar_curso, name='verificar-curso'),
    path('verificar/peticion/<str:slug>/', verificar_peticion, name='verificar-peticion'),
    path('verificar/resultado/<str:slug>/', verificar_resultado, name='verificar-resultado'),
    path('verificar/sala/<str:slug>/', verificar_sala, name='verificar-sala'),
    path('verificar/reporte/<str:slug>/', verificar_reporte, name='verificar-reporte'),
    path('verificar/contenido/individual/<str:slug>/', verificar_contenido_individual, name='verificar_contenido_individual'),
    path('cargar_contenido_individual/<str:slug>/', contenido_individual, name='cargar_individual'),
    path('cargar_contenido_principal/<str:slug>/', contenido_principal, name='cargar_principal'),
    path('codigo/contenido/<int:codigo>/', obtener_contenido_individual, name='obtener-contenido-individual'),
    path('obtener/curso/<int:id>/', obtener_slug_curso, name='obtener-slug-curso'),
    path('obtener/dominio/<str:slug>/', obtener_slug_dominio, name='obtener-slug-dominio'),
    path('obtener/contenido/<str:slug>/', obtener_slug_contenido, name='obtener-slug-contenido'),

    ### VERIFICACIONES ###
    path('verificar/inscripcion/', verificacion_inscripcion, name='verificar-inscripcion'),
    path('atender/peticion/', atender_peticion, name='atender-peticion'),
    path('atender/sala/<str:slug>/', atender_sala, name='atender-sala'),

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
