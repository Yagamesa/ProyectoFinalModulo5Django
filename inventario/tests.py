from django.test import TestCase
from .models import Categoria


class TestCategoria(TestCase):
    def test_categoria(self):
        q = Categoria(nombre="Bebidas")
        q.save()

        self.assertEqual(Categoria.objects.count(), 1)
