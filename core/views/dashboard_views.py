"""
Vista principal del Dashboard para El Restaurante de Django (FORMO DEV).
Consulta los modelos de la app 'restaurante' y prepara el contexto para la plantilla.
"""

from django.shortcuts import render
from restaurante.models import Menu, Pedido

def dashboard(request):
    """
    Vista principal (El Cocinero preparando todo para el Mozo/Template).
    Consulta la despensa (Modelos) y envía los datos necesarios a la plantilla.
    """
    platos = Menu.objects.filter(tipo='PLATO', disponible=True).order_by('nombre')
    bebidas = Menu.objects.filter(tipo='BEBIDA', disponible=True).order_by('nombre')

    pedidos_pendientes = Pedido.objects.filter(estado='PENDIENTE').select_related('plato', 'bebida')
    pedidos_preparando = Pedido.objects.filter(estado='PREPARANDO').select_related('plato', 'bebida')
    pedidos_servidos = Pedido.objects.filter(estado='SERVIDO').select_related('plato', 'bebida')

    context = {
        'platos': platos,
        'bebidas': bebidas,
        'pedidos_pendientes': pedidos_pendientes,
        'pedidos_preparando': pedidos_preparando,
        'pedidos_servidos': pedidos_servidos,
        'total_pendientes': pedidos_pendientes.count(),
        'total_preparando': pedidos_preparando.count(),
        'total_servidos': pedidos_servidos.count(),
        'total_pedidos': Pedido.objects.count(),
        'total_menu': Menu.objects.count(),
    }
    return render(request, 'restaurante/dashboard.html', context)
