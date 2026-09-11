"""
Proxy de retrocompatibilidad hacia la app 'notificaciones'.
"""
from notificaciones.consumers import DesafioProgressConsumer
from notificaciones.services import notificar_avance_usuario

__all__ = ['DesafioProgressConsumer', 'notificar_avance_usuario']
