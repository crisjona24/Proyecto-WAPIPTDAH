import random
from django.db import IntegrityError
from .models import *
from .serializer import *
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, generics
from django.contrib.auth import authenticate, login, logout
import re
from django.http import HttpResponse, JsonResponse
from django.urls import reverse

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

# Token de verificacion de cuenta
from django.core.signing import Signer, BadSignature


## METODOS VARIOS ###
def es_correo_valido(correo):
    er = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    if re.match(er, correo) is not None:
        return True
    else:
        return False

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
                    refresh=RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    # Verificamos el tipo de usuario
                    if is_paciente(user):
                        user_ob = Paciente.objects.get(user=user)
                        if user_ob.is_activo:
                            context = {
                                'success': True,
                                'tipo': 'paciente',
                                'token': access_token,
                            }
                            return JsonResponse(context)
                        else:
                            context = {
                                'error': 'El usuario no esta activo',
                            }
                            return JsonResponse(context, status=401)
                    elif is_tecnico(user):
                        user_ob = Usuario.objects.get(user=user)
                        if user_ob.is_activo:
                            context = {
                                'success': True,
                                'tipo': 'tecnico',
                                'token': access_token,
                            }
                            return JsonResponse(context)
                        else:
                            context = {
                                'error': 'El usuario no esta activo',
                            }
                            return JsonResponse(context, status=401)
                    elif is_comun(user):
                        user_ob = UsuarioComun.objects.get(user=user)
                        if user_ob.is_activo:
                            context = {
                                'success': True,
                                'tipo': 'comun',
                                'token': access_token,
                            }
                            return JsonResponse(context)
                        else:
                            context = {
                                'error': 'El usuario no esta activo',
                            }
                            return JsonResponse(context, status=401)
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
            if is_comun(user) or is_tecnico(user):
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


def validar_correo_link(_email):
    try:
        signer = Signer()
        token_firmado = signer.sign(_email)
        # Email
        subject = 'Confirmación de cuenta'
        #message = f'Haz clic en el siguiente enlace para verificar tu cuenta: {settings.SITE_URL}/verificar/{token_firmado}'
        message = f'Copia y pega el siguiente código especial para verificar tu cuenta: {token_firmado}'
        from_email = settings.EMAIL_HOST_USER
        receiver_email = [_email]
        send_mail(subject, message, from_email, receiver_email, fail_silently=False)
        return True
    except Exception as e:
        print(f"Error enviando el correo: {e}")
        return False

@api_view(['POST'])
def verificar_email_firmado(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            token = data.get('tokenVerificacion')
            signer = Signer()
            email_original = signer.unsign(token)
            user_ob = User.objects.get(email=email_original)
            if is_tecnico(user_ob):
                usuario__ob = Usuario.objects.get(user=user_ob)
                if verificado_correo(usuario__ob):
                    return JsonResponse({'error': 'El usuario ya esta activo'})
                usuario__ob.is_activo = True
                usuario__ob.save()
                return JsonResponse({'success': True})
            elif is_paciente(user_ob):
                paciente__ob = Paciente.objects.get(user=user_ob)
                if verificado_correo(paciente__ob):
                    return JsonResponse({'error': 'El usuario ya esta activo'})
                paciente__ob.is_activo = True
                paciente__ob.save()
                return JsonResponse({'success': True})
            elif is_comun(user_ob):
                comun__ob = UsuarioComun.objects.get(user=user_ob)
                if verificado_correo(comun__ob):
                    return JsonResponse({'error': 'El usuario ya esta activo'})
                comun__ob.is_activo = True
                comun__ob.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'Código de verificación inválido o ha expirado'})
        else: 
            return JsonResponse({'error': 'Código de verificación inválido o ha expirado'})
    except BadSignature:
       return JsonResponse({'error': 'Código de verificación inválido o ha expirado'})


def verificado_correo(ob1):
    # verificar si el objeto usuario esta activo
    if ob1.is_activo:
        return True
    else:
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
            # Veriicar correo valido
            if es_correo_valido(email_) == False:
                return JsonResponse({'correo': 'Correo invalido'})
            # Verificar clave
            if validar_clave(password_) == False:
                return JsonResponse({'clave': 'Clave sin requisitos mínimos'})
            # Verificar si el usuario ya existe
            if existe__registro(first_name_, last_name_):
                return JsonResponse({'error': 'El usuario ya existe'})
            else:
                if username_exist(username_):
                    return JsonResponse({'error': 'El nombre de usuario ya existe'})
                else:
                    # Verificar confirmacion de cuenta
                    if not validar_correo_link(email_):
                        return JsonResponse({'error': 'El correo es invalido o no existe'})
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
            # Veriicar correo valido
            if es_correo_valido(email_) == False:
                return JsonResponse({'correo': 'Correo invalido'})
            # Verificar clave
            if validar_clave(password_) == False:
                return JsonResponse({'clave': 'Clave sin requisitos mínimos'})
            # Verificar si el usuario ya existe
            if existe__registro(first_name_, last_name_):
                return JsonResponse({'error': 'El usuario ya existe'})
            else:
                if username_exist(username_):
                    return JsonResponse({'error': 'El nombre de usuario ya existe'})
                else:
                    # Verificar confirmacion de cuenta
                    if not validar_correo_link(email_):
                        return JsonResponse({'error': 'El correo es invalido o no existe'})
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
            # Veriicar correo valido
            if es_correo_valido(email_) == False:
                return JsonResponse({'correo': 'Correo invalido'})
            # Verificar clave
            if validar_clave(password_) == False:
                return JsonResponse({'clave': 'Clave sin requisitos mínimos'})
            # Verificar si el usuario ya existe
            if existe__registro(first_name_, last_name_):
                return JsonResponse({'error': 'El usuario ya existe'})
            else:
                if username_exist(username_):
                    return JsonResponse({'error': 'El nombre de usuario ya existe'})
                else:
                    # Verificar confirmacion de cuenta
                    if not validar_correo_link(email_):
                        return JsonResponse({'error': 'El correo es invalido o no existe'})
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
                        if control_categorias():
                            # Creamos el contenido
                            if guardar_dominio(nombre_dominio_, identificador_, descripcion_, portada_, usuario__ob):
                                return JsonResponse({'success': True})
                            else:
                                return JsonResponse({'error': 'Error al guardar el dominio'})
                        else:
                            return JsonResponse({'error': 'No se puede registrar el dominio porque se excede lo permitido'})
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

def control_categorias():
    try:
        # Obtenemos los registros de nivel
        grado__ob = GradoTDAH.objects.all()
        # Buscamos el numero_categorias de los niveles
        numero_categorias_ = 0
        for grado in grado__ob:
            numero_categorias_ = grado.numero_categorias
        # Buscamos el numero de dominios registrados
        dominiio_ob = Dominio.objects.all()
        numero_dominios_ = dominiio_ob.count()
        # Verificar si el numero de dominios es menor al numero de categorias
        if numero_dominios_ < numero_categorias_:
            return True
        else:
            return False
    except GradoTDAH.DoesNotExist:
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
                    img1_ = request.FILES.get('img1')
                    img2_ = request.FILES.get('img2')
                    img3_ = request.FILES.get('img3')
                    img4_ = request.FILES.get('img4')
                    img5_ = request.FILES.get('img5')
                    portada_ = request.FILES.get('portada_individual')
                    pertenece_ = request.POST.get('conten')
                    nombre_nivel_ = request.POST.get('nombre_nivel')
                    # Obtenemos el objeto contenido por el nombre
                    contenido__ob = Contenido.objects.get(nombre=pertenece_)
                    # Calculamos el identificador
                    identificador_ = generar_identificador_individual()
                    # Creamos el contenido
                    if tipocontenido_ == 'pintar_imagen':
                        if guardar_contenido_individual_4(descripcion_, identificador_, tipocontenido_, contenido_, 
                                                        portada_, respuesta_, nombre_nivel_, contenido__ob,
                                                         img1_):
                            return JsonResponse({'success': True})
                        else:
                            return JsonResponse({'error': 'Error al guardar el contenido individual'})
                    elif tipocontenido_ == 'seleccionar_imagen':
                        # Para imagen 1, 2 y 3 y que no exista imagen 4 y 5
                        if img1_ and img2_ and img3_ and not img4_ and not img5_:
                            if guardar_contenido_individual_2(descripcion_, identificador_, tipocontenido_, contenido_, 
                                                            portada_, respuesta_, nombre_nivel_, contenido__ob, img1_, img2_, img3_):
                                return JsonResponse({'success': True})
                            else:
                                return JsonResponse({'error': 'Error al guardar el contenido individual'})
                        elif img1_ and img2_ and img3_ and img4_ and img5_:
                            if guardar_contenido_individual_3(descripcion_, identificador_, tipocontenido_, contenido_, 
                                                            portada_, respuesta_, nombre_nivel_, contenido__ob, img1_, img2_, img3_):
                                return JsonResponse({'success': True})
                            else:
                                return JsonResponse({'error': 'Error al guardar el contenido individual'})
                        else:
                            return JsonResponse({'error': 'Error al guardar el contenido individual'})
                    else:
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

def guardar_contenido_individual_2(ob1, ob2, ob3, ob4, ob5, ob6, ob7, ob8, ob9, ob10, ob11):
    try:
        contenido_individual = ContenidoIndividual.objects.create(
            descripcion_individual=ob1,
            identificador_individual=ob2,
            tipo_contenido=ob3,
            contenido_individual=ob4,
            imagen1=ob9,
            imagen2=ob10,
            imagen3=ob11,
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

def guardar_contenido_individual_3(ob1, ob2, ob3, ob4, ob5, ob6, ob7, ob8, ob9, ob10, ob11, ob12, ob13):
    try:
        contenido_individual = ContenidoIndividual.objects.create(
            descripcion_individual=ob1,
            identificador_individual=ob2,
            tipo_contenido=ob3,
            contenido_individual=ob4,
            imagen1=ob9,
            imagen2=ob10,
            imagen3=ob11,
            imagen4=ob12,
            imagen5=ob13,
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

def guardar_contenido_individual_4(ob1, ob2, ob3, ob4, ob5, ob6, ob7, ob8, ob9):
    try:
        contenido_individual = ContenidoIndividual.objects.create(
            descripcion_individual=ob1,
            identificador_individual=ob2,
            tipo_contenido=ob3,
            contenido_individual=ob4,
            imagen1=ob9,
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
                elif (contenidoI__ob.tipo_contenido == 'seleccionar_imagen'):
                    url_c1 = cloudinary.CloudinaryImage(contenidoI__ob.imagen1.name).build_url()
                    url_c2 = cloudinary.CloudinaryImage(contenidoI__ob.imagen2.name).build_url()
                    url_c3 = cloudinary.CloudinaryImage(contenidoI__ob.imagen3.name).build_url()
                    url_c4 = cloudinary.CloudinaryImage(contenidoI__ob.imagen4.name).build_url()
                    url_c5 = cloudinary.CloudinaryImage(contenidoI__ob.imagen5.name).build_url()
                    context.update({'tipo': 'seleccionar_imagen', 'url_c1': url_c1, 
                                    'url_c2': url_c2, 'url_c3': url_c3, 'url_c4': url_c4, 'url_c5': url_c5})
                    return JsonResponse(context)
                elif (contenidoI__ob.tipo_contenido == 'responder_preguntas'):
                    context.update({'tipo': 'responder_preguntas'})
                    return JsonResponse(context)
                elif (contenidoI__ob.tipo_contenido == 'pintar_imagen'):
                    url_c1 = cloudinary.CloudinaryImage(contenidoI__ob.imagen1.name).build_url()
                    context.update({'tipo': 'pintar_imagen', 'url_c1': url_c1})
                    return JsonResponse(context)
                elif (contenidoI__ob.tipo_contenido == 'cuento'):
                    context.update({'tipo': 'cuento'})
                    return JsonResponse(context)
                elif (contenidoI__ob.tipo_contenido == 'selecion_multiple_img'):
                    url_c1 = cloudinary.CloudinaryImage(contenidoI__ob.imagen1.name).build_url()
                    url_c2 = cloudinary.CloudinaryImage(contenidoI__ob.imagen2.name).build_url()
                    url_c3 = cloudinary.CloudinaryImage(contenidoI__ob.imagen3.name).build_url()
                    context.update({'tipo': 'selecion_multiple_img', 'url_c1': url_c1, 'url_c2': url_c2, 'url_c3': url_c3})
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

        # Verificar si existen multiples codigos identificadores separados por coma o un solo codigo
        if comprobar_separacion_coma(codigo_identificador_):
            identificadores_separados = codigo_identificador_.split(', ')
            # Cada identificador debe convertirse en dato entero
            for identificador in identificadores_separados:
                # Convertir identificador en entero
                identificador = int(identificador)
                if not identificador_existe(identificador):
                    return JsonResponse({'error': "El contenido que requiere evaluar no existe. Ingresa un identificador válido."})
        else:
            codigo_ = int(codigo_identificador_)
            if not identificador_existe(codigo_):
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


## METODO DE EDICION DE SALA
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def api_sala_edicion(request):
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
        identificador_sala_ = data.get('identificador_sala')

        if not curso_existe(usuario__ob):
            return JsonResponse({'error': "No tiene un curso registrado. No puede registrar salas."})

        # Verificar si existen multiples codigos identificadores separados por coma o un solo codigo
        if comprobar_separacion_coma(codigo_identificador_):
            identificadores_separados = codigo_identificador_.split(', ')
            # Cada identificador debe convertirse en dato entero
            for identificador in identificadores_separados:
                # Convertir identificador en entero
                identificador = int(identificador)
                if not identificador_existe(identificador):
                    return JsonResponse({'error': "El contenido que requiere evaluar no existe. Ingresa un identificador válido."})
        else:
            codigo_ = int(codigo_identificador_)
            if not identificador_existe(codigo_):
                return JsonResponse({'error': "El contenido que requiere evaluar no existe. Ingresa un identificador válido."})        
            
        if nombresala_exist_edicion(nombre_sala_, identificador_sala_):
            return JsonResponse({'error': "El nombre de la sala ya existe. Ingresa otro nombre."})
        
        try: 
            if actualizar_sala(nombre_sala_, anotaciones_, codigo_identificador_, identificador_sala_):
                # Enviamos una respuesta al front
                return JsonResponse({'success': True})
            else:
                error_message = "Error al editar sala."
                context = {'error': error_message}
                return JsonResponse(context)
        except Exception as e:
            print(e)
            return JsonResponse({'error': "Algo salió mal"})
    else:
        return JsonResponse({'error': 'El usuario no está autenticado'})

def actualizar_sala(ob1, ob2, ob3, ob4):
    try:
        sala_obj = Sala.objects.get(id=ob4)
        sala_obj.nombre_sala = ob1
        sala_obj.anotaciones = ob2
        sala_obj.codigo_identificador = ob3
        sala_obj.save()
        return True
    except Exception as e:
        return False

def nombresala_exist_edicion(ob1, ob2):
    try:
        # Buscamos el objeto sala
        sala__ob = Sala.objects.get(id=ob2)
        # Comparar si el nombre del registro es el mismo que viene en el request muestra falso
        if sala__ob.nombre_sala == ob1:
            return False
        # Buscamos si existe el nombre de la sala y que no sea el nombre del registro ya existente
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
    

## ENVIAR CORREO DE CONTACTO
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def api_enviar_contacto(request):
    if request.user.is_authenticated:
        # Obtenemos el token
        try:
            token = request.headers.get('Authorization').split(" ")[1]
            user = get_user_from_token_jwt(token)
        except Exception as e:
            return JsonResponse({'error': 'El usuario no está autenticado'})
        
        # Verificar metodo permitido
        if request.method != 'POST':
            return JsonResponse({'error': 'Método no permitido'})

        # Encontrar al usuario relacionado al user
        usuario__ob = encontrar_usuario(user)
        if usuario__ob:
            if request.method == 'POST':
                data = json.loads(request.body)
                asunto_ = data.get('motivo')
                mensaje_ = data.get('cuerpo')
                if enviar_correo(usuario__ob, asunto_, mensaje_):
                    return JsonResponse({'success': True})
                else:
                    error_message = "Error al enviar el correo."
                    context = {'error': error_message}
                    return JsonResponse(context)
            else:
                return JsonResponse({'error': 'No es posible ejecutar la acción'}, status=405)
        else:
            return JsonResponse({'error': 'Usuario no encontrado'})
    else:
        return JsonResponse({'error': 'El usuario no está autenticado'})

def encontrar_usuario(ob1):
    # Orden de los modelos a verificar
    modelos = [UsuarioComun, Paciente, Usuario]

    for modelo in modelos:
        try:
            # Intenta obtener el usuario de cada modelo
            usuario_ob = modelo.objects.get(user=ob1)
            return usuario_ob
        except modelo.DoesNotExist:
            # Si el usuario no existe en ese modelo, sigue con el siguiente
            continue

    # Si ninguno de los modelos contiene el usuario, retorna False
    return False

def enviar_correo(ob1, ob2, ob3):
    # Capturamos los datos para el email
    subject = ob2
    message = ob3
    from_email = ob1.email_usuario
    print(ob1.email_usuario)
    receiver_email = [settings.EMAIL_HOST_USER]

    send_mail(subject, message, from_email, receiver_email, fail_silently=False)
    return True



## GENERAR REPORTE ##
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def generar_reporte_resultado(request, id):
    try: 
        # Decodifica el token
        token = request.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        # Verificar existencia del usuario
        if user and token:
            if request.method == 'GET':
                id_resultado_ = id
                # Guardar Reporte
                if guardar_reporte(id_resultado_, user):
                    return JsonResponse({'success': True})
                else:
                    error_message = "Error al generar el reporte...."
                    context = {'error': error_message}
                    return JsonResponse(context)
            else:
                return JsonResponse({'error': 'No es posible ejecutar la acción'}, status=405)
        else:
            return JsonResponse({'error': 'El usuario no se ha autenticado'}, status=401)
    except Exception as e:
        return JsonResponse({'error': 'Ups! algo salió mal'}, status=500)

def guardar_reporte(ob1, ob2):
    try:
        #Obtenemos el objeto resultado
        resultado_ob = Resultado.objects.get(id=ob1)
        # Obtenemos datos necesarios para el reporte
        paciente_ob = resultado_ob.paciente
        contenido_individual_ob = resultado_ob.contenido_individual
        usuario_comun_ob = UsuarioComun.objects.get(user=ob2)
        # Creamos el reporte
        reporte_ob = Reporte.objects.create(
            titulo_reporte = "Reporte de Resultado",
            descripcion_reporte = "No hay una descripción, debe ser agregada.",
            usuario_comun = usuario_comun_ob,
            contenido_individual = contenido_individual_ob,
            paciente = paciente_ob,
            resultado = resultado_ob
        )
        reporte_ob.save()
        # Modifiamos el estado de reporte del resultado
        resultado_ob.estado_reporte = True
        resultado_ob.save()
        return True
    except Exception as e:
        return False


## GENERAR REPORTE ##
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def modificar_estado_reporte(request, id):
    try: 
        # Decodifica el token
        token = request.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        # Verificar existencia del usuario
        if user and token:
            if request.method == 'GET':
                id_reporte = id
                # Guardar Reporte
                if modificar_estado_resultado(id_reporte):
                    return JsonResponse({'success': True})
                else:
                    error_message = "Error al eliminar el reporte...."
                    context = {'error': error_message}
                    return JsonResponse(context)
            else:
                return JsonResponse({'error': 'No es posible ejecutar la acción'}, status=405)
        else:
            return JsonResponse({'error': 'El usuario no se ha autenticado'}, status=401)
    except Exception as e:
        return JsonResponse({'error': 'Ups! algo salió mal'}, status=500)
    
def modificar_estado_resultado(ob1):
    try:
        #Obtenemos el objeto reporte a partir del id
        reporte_ob = Reporte.objects.get(id=ob1)
        # Obtenemos el objeto resultado relacionado al reporte
        resultado_ob = reporte_ob.resultado
        # Modifiamos el estado de reporte del resultado
        resultado_ob.estado_reporte = False
        resultado_ob.save()
        return True
    except Exception as e:
        return False


## GENERAR REPORTE POR NOMBRE DE PACIENTE ##
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def generar_reporte_all(request):
    try: 
        # Decodifica el token
        token = request.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        # Verificar existencia del usuario
        if user and token:
            # Verificar que sea usuario comun
            if (is_comun(user)):
                if request.method == 'POST':
                    # Obtener el valor del nombre del paciente
                    data = json.loads(request.body)
                    nombre_paciente_ = data.get('nombre')
                    # Obtener el nombre y apellido del paciente de nombre_paciente
                    nombres_apellido = nombre_paciente_.split(' ')
                    nombre = nombres_apellido[0]
                    apellido = nombres_apellido[1]
                    # Obtener el paciente
                    paciente_ob = Paciente.objects.get(nombre_usuario__iexact=nombre, apellido_usuario__iexact=apellido)
                    # Obtener los resultados del paciente filtrando la observacion en no nulo o la obseravion diga No resuelto
                    resultados = Resultado.objects.filter(paciente=paciente_ob, observacion__isnull=False, estado_reporte=False).exclude(observacion__iexact="No resuelto")
                    print("nombre :", nombre)
                    print("apellido :", apellido)
                    if (verificar_paciente_curso(nombre, apellido, user)):
                        # Se crea el reporte por cada resultado
                        for resultado in resultados:
                            guardar_reporte(resultado.id, user)
                        return JsonResponse({'success': True})
                    else:
                        error_message = "El estudiante no se encuentra inscrito en un curso o no existe."
                        context = {'error': error_message}
                        return JsonResponse(context)
                else:
                    return JsonResponse({'error': 'No es posible ejecutar la acción'}, status=405)
            else:
                return JsonResponse({'error': 'El usuario no ha autenticado'})
        else:
            return JsonResponse({'error': 'El usuario no se ha autenticado'}, status=401)
    except Exception as e:
        return JsonResponse({'error': 'Ups! algo salió mal'}, status=500)

def verificar_paciente_curso(ob1, ob2, ob3):
    try:
        # Obtenemos el paciente
        paciente_ = Paciente.objects.get(nombre_usuario__iexact=ob1, apellido_usuario__iexact=ob2)
        # Obtenemos el usuario comun asociado
        usuario_comun_ = UsuarioComun.objects.get(user=ob3)
        # Obtener los cursos registrados por el usuario
        cursos = Curso.objects.filter(usuario_comun=usuario_comun_)
        # Obtener los paciente inscritos en los cursos creados por el usuario comun
        for curso in cursos:
            if DetalleInscripcionCurso.objects.filter(curso=curso, paciente=paciente_).exists():
                return True
        return False
    except Paciente.DoesNotExist:
        return False
    except UsuarioComun.DoesNotExist:
        return False
    except Curso.DoesNotExist:
        return False
    except DetalleInscripcionCurso.DoesNotExist:
        return False