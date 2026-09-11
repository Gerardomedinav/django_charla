import json
from django.test import TestCase, Client
from django.urls import reverse
from restaurante.models import Menu, Pedido
from restaurante.chatbot import SenseiFormoseno

class RestauranteModelTests(TestCase):
    def setUp(self):
        self.plato = Menu.objects.create(
            nombre="Empanadas Formoseñas",
            tipo="PLATO",
            precio=3500.00,
            icono="🥟"
        )
        self.bebida = Menu.objects.create(
            nombre="Tereré Clásico",
            tipo="BEBIDA",
            precio=1500.00,
            icono="🌿"
        )

    def test_creacion_menu(self):
        self.assertEqual(str(self.plato), "🥟 Empanadas Formoseñas - $3500.0")
        self.assertTrue(self.plato.disponible)

    def test_flujo_pedido_avanzar_estado(self):
        pedido = Pedido.objects.create(
            cliente_name="Valeria Test",
            mesa=2,
            plato=self.plato,
            bebida=self.bebida,
            estado="PENDIENTE"
        )
        self.assertEqual(pedido.estado, "PENDIENTE")

        # Avanzar a PREPARANDO
        nuevo = pedido.avanzar_estado()
        self.assertEqual(nuevo, "PREPARANDO")
        pedido.refresh_from_db()
        self.assertEqual(pedido.estado, "PREPARANDO")

        # Avanzar a SERVIDO
        nuevo = pedido.avanzar_estado()
        self.assertEqual(nuevo, "SERVIDO")
        pedido.refresh_from_db()
        self.assertEqual(pedido.estado, "SERVIDO")


class RestauranteViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.plato = Menu.objects.create(
            nombre="Chipá Guazú",
            tipo="PLATO",
            precio=4200.00,
            icono="🧀"
        )
        self.bebida = Menu.objects.create(
            nombre="Mate Dulce",
            tipo="BEBIDA",
            precio=1400.00,
            icono="🧉"
        )

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "El Restaurante de Django")
        self.assertContains(response, "Chipá Guazú")

    def test_tomar_pedido_ajax(self):
        payload = {
            "cliente_name": "Marcos Test",
            "mesa": 4,
            "plato_id": self.plato.id,
            "bebida_id": self.bebida.id,
            "notas": "Sin azúcar"
        }
        response = self.client.post(
            reverse('tomar_pedido'),
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['pedido']['cliente_name'], "Marcos Test")
        self.assertEqual(Pedido.objects.count(), 1)

    def test_api_pedidos(self):
        Pedido.objects.create(
            cliente_name="Gero",
            mesa=1,
            plato=self.plato,
            bebida=self.bebida,
            estado="PENDIENTE"
        )
        response = self.client.get(reverse('api_pedidos'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['pedidos']), 1)
        self.assertEqual(data['pedidos'][0]['cliente_name'], "Gero")

    def test_api_chatbot(self):
        # Consulta sobre MVT
        response = self.client.post(
            reverse('api_chatbot'),
            data=json.dumps({"mensaje": "¿Cómo es la analogía MVT del restaurante?"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("MVT", data['respuesta'])
        self.assertIn("Cocinero", data['respuesta'])

    def test_api_terminal_desafios(self):
        # Desafío 1: cd restaurante
        res1 = self.client.post(
            reverse('api_terminal'),
            data=json.dumps({"comando": "cd restaurante", "mision_actual": 1}),
            content_type="application/json"
        )
        self.assertEqual(res1.status_code, 200)
        d1 = res1.json()
        self.assertTrue(d1['mision_completada'])
        self.assertEqual(d1['siguiente_mision'], 2)

        # Desafío 2: ls
        res2 = self.client.post(
            reverse('api_terminal'),
            data=json.dumps({"comando": "ls", "mision_actual": 2}),
            content_type="application/json"
        )
        self.assertEqual(res2.status_code, 200)
        d2 = res2.json()
        self.assertTrue(d2['mision_completada'])
        self.assertEqual(d2['siguiente_mision'], 3)

    def test_api_terminal_comando_valido_explicacion(self):
        # Probar comando válido de Linux/Git que no es ninguna de las 8 misiones activas
        res = self.client.post(
            reverse('api_terminal'),
            data=json.dumps({"comando": "git status", "mision_actual": 1}),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertFalse(data['mision_completada'])
        self.assertIn("COMANDO VÁLIDO RECONOCIDO", data['output'])
        self.assertIn("¿Para qué sirve?", data['output'])
        self.assertIn("NO es la consigna de la Misión 1", data['output'])
        self.assertIn("cd restaurante", data['output'])

    def test_api_terminal_comando_otra_mision(self):
        # Probar comando de Misión 4 cuando se está en Misión 1
        res = self.client.post(
            reverse('api_terminal'),
            data=json.dumps({"comando": "python manage.py migrate", "mision_actual": 1}),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertFalse(data['mision_completada'])
        self.assertIn("COMANDO VÁLIDO DE OTRA MISIÓN", data['output'])
        self.assertIn("Misión 4", data['output'])
        self.assertIn("cd restaurante", data['output'])

    def test_api_notificar_desafio(self):
        res = self.client.post(
            reverse('api_notificar_desafio'),
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

    def test_api_terminal_comando_reset(self):
        res = self.client.post(
            reverse('api_terminal'),
            data=json.dumps({"comando": "reset", "mision_actual": 3}),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['action'], 'reset')
        self.assertEqual(data['mision_actual'], 1)
        self.assertEqual(data['siguiente_mision'], 1)
        self.assertIn("LABORATORIO REINICIADO", data['output'])



