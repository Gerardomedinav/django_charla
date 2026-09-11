import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .services import notificar_avance_usuario

@csrf_exempt
def api_notificar_desafio(request):
    """
    Disparador manual de notificaciones push WebSocket hacia clientes conectados.
    Útil para pruebas de QA, Frontend y demostraciones en vivo.
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("Método no permitido. Se requiere POST.")
    try:
        data = json.loads(request.body)
    except Exception:
        data = request.POST

    tipo = data.get('tipo', 'desafio_completado')
    desafio = data.get('nombre_desafio', 'Desafío de Laboratorio')
    try:
        progreso = int(data.get('progreso', 50))
    except (ValueError, TypeError):
        progreso = 50
    frase = data.get('frase', '¡Tereré terere, a meterle pila que vamos por más!')
    svg = data.get('svg', '/static/images/sensei_aprobando.svg')

    notificar_avance_usuario(tipo, nombre_desafio=desafio, progreso=progreso, frase=frase, svg=svg)

    return JsonResponse({
        'status': 'success',
        'message': 'Notificación push emitida exitosamente vía WebSocket',
        'payload': {
            'tipo': tipo,
            'nombre_desafio': desafio,
            'progreso': progreso,
            'frase': frase,
            'svg': svg
        }
    })
