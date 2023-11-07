from django.urls import path, include
from .views import *


urlpatterns = [
    path('juego/invasion/', Iniciar_Juego1, name='Iniciar_Juego1'),
]
