"""
Rutas específicas de la aplicación Restaurante (Gestión de comandas y catálogo).
"""
from django.urls import path
from .views import pedido_views, menu_views

app_name = 'restaurante'

urlpatterns = [
    path('tomar-pedido/', pedido_views.tomar_pedido, name='tomar_pedido'),
    path('cambiar-estado-pedido/<int:pedido_id>/', pedido_views.cambiar_estado_pedido, name='cambiar_estado_pedido'),
    path('eliminar-pedido/<int:pedido_id>/', pedido_views.eliminar_pedido, name='eliminar_pedido'),
    path('api/pedidos/', menu_views.api_pedidos, name='api_pedidos'),
    path('api/menu/', menu_views.api_menu, name='api_menu'),
]
