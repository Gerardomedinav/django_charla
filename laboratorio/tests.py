import json
from django.test import TestCase, Client
from django.urls import reverse

class LaboratorioTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_api_chatbot(self):
        response = self.client.post(
            reverse('laboratorio:api_chatbot'),
            data=json.dumps({"mensaje": "¿Cómo es la analogía MVT del restaurante?"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("MVT", data['respuesta'])
        self.assertIn("Cocinero", data['respuesta'])

    def test_api_terminal_desafio1(self):
        res = self.client.post(
            reverse('laboratorio:api_terminal'),
            data=json.dumps({"comando": "cd restaurante", "mision_actual": 1}),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['mision_completada'])
        self.assertEqual(data['siguiente_mision'], 2)

    def test_api_terminal_desafio_final(self):
        res = self.client.post(
            reverse('laboratorio:api_terminal'),
            data=json.dumps({"comando": "python manage.py seed_data", "mision_actual": 8}),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['mision_completada'])
        self.assertEqual(data['siguiente_mision'], 9)

    def test_api_terminal_reset(self):
        res = self.client.post(
            reverse('laboratorio:api_terminal'),
            data=json.dumps({"comando": "reset", "mision_actual": 3}),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['action'], 'reset')
        self.assertEqual(data['mision_actual'], 1)

