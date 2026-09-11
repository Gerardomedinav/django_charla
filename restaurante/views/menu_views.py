from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from restaurante.models import Menu, Pedido
from .pedido_views import tomar_pedido

@csrf_exempt
def api_pedidos(request):
    """
    Endpoint RESTful para comandas:
    - GET: Retorna la lista de pedidos en JSON para sincronización en tiempo real.
    - POST: Permite registrar un nuevo pedido vía JSON (QA y Frontend).
    """
    if request.method == 'POST':
        return tomar_pedido(request)

    pedidos = Pedido.objects.all().select_related('plato', 'bebida')
    data = []
    for p in pedidos:
        data.append({
            'id': p.id,
            'cliente_name': p.cliente_name,
            'mesa': p.mesa,
            'plato': p.plato.nombre if p.plato else 'Sin plato',
            'plato_icono': p.plato.icono if p.plato else '🍽️',
            'bebida': p.bebida.nombre if p.bebida else 'Sin bebida',
            'bebida_icono': p.bebida.icono if p.bebida else '🥤',
            'notas': p.notas,
            'estado': p.estado,
            'hora': p.creado_en.strftime('%H:%M'),
        })
    return JsonResponse({'pedidos': data})


def api_menu(request):
    """
    Retorna el catálogo completo de platos y bebidas para QA y Frontend.
    """
    items = []
    for m in Menu.objects.filter(disponible=True).order_by('tipo', 'nombre'):
        items.append({
            'id': m.id,
            'nombre': m.nombre,
            'tipo': m.tipo,
            'precio': str(m.precio),
            'icono': m.icono,
            'descripcion': m.descripcion,
        })
    return JsonResponse({'menu': items})
