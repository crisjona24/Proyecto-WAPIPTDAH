from celery import shared_task
from django.utils import timezone
from .models import Verificacion

# Configurar tarea de registro de usuario vencido
@shared_task
def eliminar_usuarios_vencidos():
    # Obtener fecha actual
    fecha_actual = timezone.now()
    # Obtener usuarios vencidos
    usuarios_vencidos = Verificacion.objects.filter(fecha_limite__lte=fecha_actual, atendido=False)
    # Eliminar usuarios vencidos
    for verificacion in usuarios_vencidos:
        if verificacion.usuario:
            verificacion.usuario.delete()
    return None