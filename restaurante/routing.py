"""
Proxy de retrocompatibilidad hacia las rutas websocket de 'notificaciones'.
"""
from notificaciones.routing import websocket_urlpatterns

__all__ = ['websocket_urlpatterns']
