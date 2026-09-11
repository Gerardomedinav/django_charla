import json
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from restaurante.models import Menu, Pedido

@csrf_exempt
def tomar_pedido(request):
    """
    Crea un nuevo pedido a través de formulario estándar o petición AJAX/Fetch.
    """
    if request.method == 'POST':
        # Soporte para JSON o form-data
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'JSON inválido'}, status=400)
            cliente_name = data.get('cliente_name', '').strip()
            mesa = data.get('mesa', 1)
            plato_id = data.get('plato_id')
            bebida_id = data.get('bebida_id')
            notas = data.get('notas', '').strip()
            is_ajax = True
        else:
            cliente_name = request.POST.get('cliente_name', '').strip()
            mesa = request.POST.get('mesa', 1)
            plato_id = request.POST.get('plato_id')
            bebida_id = request.POST.get('bebida_id')
            notas = request.POST.get('notas', '').strip()
            is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        if not cliente_name:
            if is_ajax:
                return JsonResponse({'success': False, 'error': 'El nombre del cliente es obligatorio.'}, status=400)
            return redirect('dashboard')

        try:
            mesa_num = int(mesa)
        except (ValueError, TypeError):
            mesa_num = 1

        plato = Menu.objects.filter(id=plato_id, tipo='PLATO').first() if plato_id else None
        bebida = Menu.objects.filter(id=bebida_id, tipo='BEBIDA').first() if bebida_id else None

        pedido = Pedido.objects.create(
            cliente_name=cliente_name,
            mesa=mesa_num,
            plato=plato,
            bebida=bebida,
            notas=notas,
            estado='PENDIENTE'
        )

        if is_ajax:
            return JsonResponse({
                'success': True,
                'message': f'¡Pedido para Mesa {pedido.mesa} registrado con éxito!',
                'pedido': {
                    'id': pedido.id,
                    'cliente_name': pedido.cliente_name,
                    'mesa': pedido.mesa,
                    'plato': pedido.plato.nombre if pedido.plato else 'Sin plato',
                    'plato_icono': pedido.plato.icono if pedido.plato else '',
                    'bebida': pedido.bebida.nombre if pedido.bebida else 'Sin bebida',
                    'bebida_icono': pedido.bebida.icono if pedido.bebida else '',
                    'notas': pedido.notas,
                    'estado': pedido.estado,
                    'hora': pedido.creado_en.strftime('%H:%M'),
                }
            })

        return redirect('dashboard')

    return redirect('dashboard')


@csrf_exempt
def cambiar_estado_pedido(request, pedido_id):
    """
    Avanza el estado del pedido: PENDIENTE -> PREPARANDO -> SERVIDO.
    """
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id)
        nuevo_estado = pedido.avanzar_estado()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({
                'success': True,
                'pedido_id': pedido.id,
                'nuevo_estado': nuevo_estado,
                'nuevo_estado_display': pedido.get_estado_display(),
            })

        return redirect('dashboard')

    return redirect('dashboard')


@csrf_exempt
def eliminar_pedido(request, pedido_id):
    """
    Elimina un pedido servido o cancelado.
    """
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id)
        pedido.delete()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({'success': True, 'pedido_id': pedido_id})

        return redirect('dashboard')

    return redirect('dashboard')
