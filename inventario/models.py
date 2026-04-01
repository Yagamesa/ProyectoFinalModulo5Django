from django.db import models
from .validators import validar_par, validar_subject, validar_cantidad
from django.core.validators import EmailValidator


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        permissions = [
            ("reporte_cantidad", "Visualizar el reporte de cantidad"),
            ("reporte_detalle", "Reporte detallado de cantidades"),
        ]


class ProductUnits(models.TextChoices):
    UNITS = 'u', 'Unidades'
    KG = 'kg', 'Kilogramos'


class Producto(models.Model):
    nombre = models.CharField(
        max_length=100,
        unique=True,
        validators=[validar_subject]  # 👈 VALIDACIÓN AGREGADA
    )
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.TextField()
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[validar_par]  # 👈 YA TENÍAS ESTA
    )
    unidades = models.CharField(
        max_length=2,
        choices=ProductUnits.choices,
        default=ProductUnits.UNITS
    )
    disponible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()])
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre


class Movimiento(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[validar_cantidad])  # 👈 VALIDACIÓN AGREGADA
    tipo = models.CharField(max_length=10, choices=[
        ('entrada', 'Entrada'),
        ('salida', 'Salida')
    ])
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre}"