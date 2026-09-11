from django.urls import path
from . import views

app_name = 'notificaciones'

urlpatterns = [
    path('api/notificar-desafio/', views.api_notificar_desafio, name='api_notificar_desafio'),
]
