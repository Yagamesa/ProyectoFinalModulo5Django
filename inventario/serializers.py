from rest_framework import serializers
from .models import Categoria, Producto, Proveedor, Movimiento
from .validators import validar_subject

# ============================
# Serializers de modelos
# ============================

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento
        fields = '__all__'

# ============================
# Serializers personalizados
# ============================

class ReporteProductoSerializer(serializers.Serializer):
    cantidad = serializers.IntegerField()
    productos = ProductoSerializer(many=True)

class ContactSerializer(serializers.Serializer):
    email = serializers.EmailField()
    subject = serializers.CharField(
        max_length=100,
        validators=[validar_subject]
    )
    body = serializers.CharField(max_length=255)