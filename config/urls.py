"""
URL Configuration raíz para el_restaurante_de_django.
Despacha de forma modular hacia las aplicaciones por dominio:
- core (dashboard general y documentación)
- restaurante (comandas, menú y pedidos)
- laboratorio (desafíos, terminal interactiva y Sensei)
- notificaciones (WebSockets y alertas en tiempo real)
"""
from django.contrib import admin
from django.urls import path, include
from core.views import dashboard_views, docs_views
from restaurante.views import pedido_views, menu_views
from laboratorio.views import terminal_views, chatbot_views
from notificaciones import views as notif_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 1. Aplicaciones Modulares con Namespaces
    path('', include('core.urls')),
    path('', include('restaurante.urls')),
    path('', include('laboratorio.urls')),
    path('', include('notificaciones.urls')),

    # 2. Rutas con prefijo de dominio explícito
    path('restaurante/', include('restaurante.urls', namespace='restaurante_domain')),
    path('laboratorio/', include('laboratorio.urls', namespace='laboratorio_domain')),
    path('notificaciones/', include('notificaciones.urls', namespace='notificaciones_domain')),

    # 3. Alias globales sin namespace (Retrocompatibilidad total para tests y scripts legados)
    path('', dashboard_views.dashboard, name='dashboard'),
    path('tomar-pedido/', pedido_views.tomar_pedido, name='tomar_pedido'),
    path('cambiar-estado-pedido/<int:pedido_id>/', pedido_views.cambiar_estado_pedido, name='cambiar_estado_pedido'),
    path('eliminar-pedido/<int:pedido_id>/', pedido_views.eliminar_pedido, name='eliminar_pedido'),
    path('api/pedidos/', menu_views.api_pedidos, name='api_pedidos'),
    path('api/menu/', menu_views.api_menu, name='api_menu'),
    path('api/chatbot/', chatbot_views.api_chatbot, name='api_chatbot'),
    path('api/terminal/', terminal_views.api_terminal, name='api_terminal'),
    path('api/seed-rapido/', terminal_views.api_seed_rapido, name='api_seed_rapido'),
    path('api/notificar-desafio/', notif_views.api_notificar_desafio, name='api_notificar_desafio'),
    path('swagger/', docs_views.swagger_ui, name='swagger_ui'),
    path('redoc/', docs_views.redoc_ui, name='redoc_ui'),
    path('api/schema.json', docs_views.openapi_schema, name='openapi_schema'),
]
