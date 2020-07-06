from django.test import TestCase, Client

# Create your tests here.
class ApiTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    def test_itworks(self):
        self.assertTrue(True)

    def test_oldgen(self):
        client = self.c
        response = client.post('/api/', content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response = client.post('/api2/', content_type='application/json')
        self.assertEqual(response.status_code, 404)