from django.test import TestCase, Client
from django.urls import reverse

class CoreTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_dashboard(self):
        response = self.client.get(reverse('core:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_swagger_ui(self):
        response = self.client.get(reverse('core:swagger_ui'))
        self.assertEqual(response.status_code, 200)

    def test_openapi_schema(self):
        response = self.client.get(reverse('core:openapi_schema'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('openapi', data)
