import json
from django.test import TestCase, Client
from django.urls import reverse

class NotificacionesTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_api_notificar_desafio(self):
        res = self.client.post(
            reverse('notificaciones:api_notificar_desafio'),
            data=json.dumps({
                "tipo": "desafio_completado",
                "nombre_desafio": "Misión 1: El Plano Arquitectónico",
                "progreso": 25,
                "frase": "¡Tereré terere, a meterle pila que vamos por más!"
            }),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['payload']['progreso'], 25)
        self.assertIn("Plano Arquitectónico", data['payload']['nombre_desafio'])
