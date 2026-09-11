"""
Paquete de Vistas para la aplicación Restaurante.
Exporta las vistas gastronómicas y mantiene retrocompatibilidad con las vistas migradas.
"""

from .pedido_views import tomar_pedido, cambiar_estado_pedido, eliminar_pedido
from .menu_views import api_pedidos, api_menu

# Proxies de retrocompatibilidad para código legado o dependencias previas
from core.views.dashboard_views import dashboard
from core.views.docs_views import swagger_ui, redoc_ui, openapi_schema
from laboratorio.views.terminal_views import api_terminal, api_seed_rapido
from laboratorio.views.chatbot_views import api_chatbot
from notificaciones.views import api_notificar_desafio

__all__ = [
    'tomar_pedido',
    'cambiar_estado_pedido',
    'eliminar_pedido',
    'api_pedidos',
    'api_menu',
    'dashboard',
    'swagger_ui',
    'redoc_ui',
    'openapi_schema',
    'api_terminal',
    'api_seed_rapido',
    'api_chatbot',
    'api_notificar_desafio',
]
