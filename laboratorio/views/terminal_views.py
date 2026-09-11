import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
from laboratorio.services.mission_service import MissionService

@csrf_exempt
def api_terminal(request):
    """
    Consola interactiva con 4 Desafíos Guiados para FORMO DEV:
    1: python manage.py makemigrations
    2: python manage.py migrate
    3: docker compose up -d (o docker-compose up -d)
    4: python manage.py seed_data
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("Método no permitido")

    try:
        data = json.loads(request.body)
    except Exception:
        data = request.POST

    cmd = data.get('comando', '').strip()
    try:
        mision_actual = int(data.get('mision_actual', 1))
    except (ValueError, TypeError):
        mision_actual = 1

    resultado = MissionService.procesar_comando(cmd, mision_actual)
    return JsonResponse(resultado)


@csrf_exempt
def api_seed_rapido(request):
    """
    Ejecuta programáticamente seed_data desde la interfaz con un clic.
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("POST requerido")

    try:
        call_command('seed_data')
        return JsonResponse({'success': True, 'message': '¡Menú y comandas de prueba cargados con éxito!'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
