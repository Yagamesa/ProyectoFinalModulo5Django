from django.test import TestCase
from .models import Categoria
from django.test import Client


class TestCategoria(TestCase):
    fixtures = ['dump_inventario.json', 'dump_auth.json']

    def setUp(self):
        self.client = Client()
        resauth = self.client.post('/api/token/', {
            "username": "admin",
            "password": "Developer"
        })
        self.token = resauth.json()["access"]
        
        # q = Categoria(nombre="Bebidas")
        # q.save()

    # def test_categoria_rest(self):
    #     response = self.client.get('/inventario/categorias/cantidad')
    #     print(response.text)
    #     assert response.json()["cantidad"] == 4
    #     assert response.status_code == 200

    def test_inventario_reporte_rest(self):
        response = self.client.get('/inventario/reporte/productos', headers={"Authorization": f"Bearer {self.token}"})
        assert response.status_code == 200

    # def test_categoria(self):
    #     q = Categoria(nombre="Bebidas")
    #     q.save()
    #
    #     self.assertEqual(Categoria.objects.count(), 1)
