from django.shortcuts import render
from Juegos.juegos import Game
from APPWapiptda.views import *
from APPWapiptda.models import *
from APPWapiptda.serializer import *
from django.contrib.auth.models import User
# from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken, Token, UntypedToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# Código de ejecución del primer juego simple integrado a la aplicación.
# Tomado de la web aplicanco ciertas modificaciones para su integración.
# Link: https://www.geeksforgeeks.org/word-guessing-game-in-python/
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def Iniciar_Juego1(request):
    try:
        # Decodifica el token para obtener el usuario
        token = request.headers.get('Authorization').split(" ")[1]
        user = get_user_from_token_jwt(token)
        # user = get_user_from_token(token)
        # Validamos si el usuario es tecnico
        if is_paciente(user):
            # Encontrar al usuario relacionado al user
            usuario__ob = Paciente.objects.get(user=user)
            # Verificar si el usuario existe
            if request.method == 'GET' and usuario__ob:
                # Creamos instancia de Game
                game = Game()
                # Iniciamos el juego
                game.__init__()
                # Retornamos el estado del juego
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'No esta permitido'})
        else:
            return JsonResponse({'error': 'El usuario no esta autenticado'})
    except Exception as e:
        return JsonResponse({'error': str(e)})
