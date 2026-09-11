import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DesafioProgressConsumer(AsyncWebsocketConsumer):
    """
    Consumer WebSocket para notificación en tiempo real de avance en los desafíos del laboratorio.
    Conecta al grupo 'chat_laboratorio_restaurante' y emite eventos con el progreso,
    estado, frase formoseña y avatar SVG dinámico del Sensei.
    """
    async def connect(self):
        self.room_name = "laboratorio_restaurante"
        self.room_group_name = f"chat_{self.room_name}"

        # Unirse al grupo de WebSocket
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Saludo inicial al cliente conectado
        await self.send(text_data=json.dumps({
            'progress': 0,
            'status': "Conectado al laboratorio en tiempo real",
            'phrase': "¡Mba'éichapa! Esperando la orden del Sensei...",
            'sensei_svg': "/static/images/sensei_esperando.svg"
        }))

    async def disconnect(self, close_code):
        # Salir del grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return
        try:
            data = json.loads(text_data)
            action = data.get('action')
            if action == 'ping':
                await self.send(text_data=json.dumps({'pong': True}))
            elif action == 'solicitar_estado':
                await self.send(text_data=json.dumps({
                    'progress': 0,
                    'status': "Laboratorio activo",
                    'phrase': "¡Elegí una misión en la terminal o completá el flujo MVT!",
                    'sensei_svg': "/static/images/sensei_esperando.svg"
                }))
        except Exception:
            pass

    # Este método se activa desde cualquier vista o tarea de Django al terminar un desafío
    async def enviar_notificacion_progreso(self, event):
        progreso = event.get('progreso', 0)
        estado = event.get('estado', 'Actualización de laboratorio')
        frase_formosena = event.get('frase_formosena', "¡Tereré con menta fresca!")
        sensei_svg = event.get('sensei_svg', '/static/images/sensei_esperando.svg')

        # Enviar los datos del desafío y el SVG del Sensei al frontend
        await self.send(text_data=json.dumps({
            'tipo': event.get('tipo', 'desafio_completado'),
            'progress': progreso,
            'status': estado,
            'phrase': frase_formosena,
            'sensei_svg': sensei_svg
        }))
