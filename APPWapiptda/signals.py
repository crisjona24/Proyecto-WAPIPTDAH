from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Peticion
from .utils import send_peticion_notification

""" 
# Verifica el estado de cambio de la peticion y devuelve un V o F
@receiver(post_save, sender=Peticion)
def send_notification(sender, instance, **kwargs):
    # Verifica si estado_revision ha sido modificado
    if 'created' in kwargs:
        if not kwargs['created'] and instance.estado_revision:
            print("La señal post_save se ha activado")
            send_peticion_notification(instance)
"""
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import cloudinary
from cloudinary import uploader
from .models import Dominio, Contenido, ContenidoIndividual

# Función de escucha de eliminación de portada de Dominio
@receiver(pre_delete, sender=Dominio)
def delete_dominio(sender, instance, **kwargs):
    print("La señal pre_delete se ha activado")
    if instance.portada_dominio:
        public_id = cloudinary.CloudinaryImage(instance.portada_dominio.name).public_id
        if public_id:
            try:
                result = uploader.destroy(public_id)
                if result.get('result') != 'ok':
                    pass
            except Exception as e:
                # Manejar cualquier excepción durante la eliminación en Cloudinary
                pass

# Función de escucha de eliminación de portada de Contenido
@receiver(pre_delete, sender=Contenido)
def delete_contenido(sender, instance, **kwargs):
    print("La señal pre_delete se ha activado")
    if instance.portada:
        public_id = cloudinary.CloudinaryImage(instance.portada.name).public_id
        if public_id:
            try:
                result = uploader.destroy(public_id)
                if result.get('result') != 'ok':
                    pass
            except Exception as e:
                # Manejar cualquier excepción durante la eliminación en Cloudinary
                pass

# Función de escucha de eliminación de imágenes de Contenido Individual
@receiver(pre_delete, sender=ContenidoIndividual)
def delete_contenido_individual(sender, instance, **kwargs):
    print("La señal pre_delete se ha activado")
    imagenes = ['portada_individual', 'contenido_individual', 'imagen1', 'imagen2', 'imagen3', 'imagen4', 'imagen5']
    for imagen_field in imagenes:
        imagen = getattr(instance, imagen_field, None)
        if imagen:
            public_id = cloudinary.CloudinaryImage(imagen.name).public_id
            if public_id:
                try:
                    result = uploader.destroy(public_id)
                    if result.get('result') != 'ok':
                        print(f"Error al eliminar la imagen {imagen_field} del objeto ContenidoIndividual")
                        pass
                except Exception as e:
                    print(f"Error durante la eliminación de la imagen {imagen_field} del objeto ContenidoIndividual: {str(e)}")
                    pass