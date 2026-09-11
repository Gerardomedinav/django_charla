import asyncio
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notificar_avance_usuario(tipo_evento, nombre_desafio="", progreso=None, frase=None, svg=None):
    """
    Disparador de notificaciones push WebSocket hacia todos los clientes del laboratorio.
    Puede ser invocado desde views, models, o comandos de terminal de Django.
    """
    channel_layer = get_channel_layer()
    if not channel_layer:
        return

    if tipo_evento == "reset":
        prog = 0
        estado = "Laboratorio reiniciado a la Misión 1"
        frase_txt = frase or "¡Tabula rasa chamigo! Empezamos desde la Misión 1 con tereré fresco."
        svg_path = svg or "/static/images/sensei_esperando.svg"

    elif tipo_evento == "desafio_completado":
        prog = progreso if progreso is not None else 50
        estado = f"¡Desafío '{nombre_desafio}' superado en el laboratorio!"
        frase_txt = frase or "¡Tereré terere, a meterle pila que vamos por más!"
        svg_path = svg or "/static/images/sensei_aprobando.svg"

    elif tipo_evento == "ejercicio_completo":
        prog = 100
        estado = "¡Ejercicio completo en el restaurante y laboratorio!"
        frase_txt = frase or "¡Artesanal, con sapucay y orgullo formoseño!"
        svg_path = svg or "/static/images/sensei_triunfando.svg"

    else:
        prog = progreso or 0
        estado = f"Avance en '{nombre_desafio}'" if nombre_desafio else "Actualización del Sensei"
        frase_txt = frase or "¡Mba'éichapa! Sigamos aprendiendo chamigo."
        svg_path = svg or "/static/images/sensei_esperando.svg"

    # Enviar al grupo de WebSockets soportando tanto contextos síncronos como asíncronos
    payload = {
        "type": "enviar_notificacion_progreso",
        "tipo": tipo_evento,
        "progreso": prog,
        "estado": estado,
        "frase_formosena": frase_txt,
        "sensei_svg": svg_path
    }

    try:
        loop = None
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            asyncio.create_task(channel_layer.group_send("chat_laboratorio_restaurante", payload))
        else:
            async_to_sync(channel_layer.group_send)("chat_laboratorio_restaurante", payload)
    except Exception as e:
        print(f"[WebSocket Error] No se pudo enviar notificación: {e}")
