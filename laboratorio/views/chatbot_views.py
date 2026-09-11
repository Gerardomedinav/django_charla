import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from laboratorio.services.chatbot_service import SenseiFormoseno

@csrf_exempt
def api_chatbot(request):
    """
    Endpoint del Sensei Formoseño.
    Recibe un mensaje y devuelve la respuesta técnica con calidez pedagógica local.
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("Método no permitido")

    try:
        data = json.loads(request.body)
        mensaje = data.get('mensaje', '')
    except Exception:
        mensaje = request.POST.get('mensaje', '')

    respuesta = SenseiFormoseno.responder(mensaje)
    return JsonResponse(respuesta)
