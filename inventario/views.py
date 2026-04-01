from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from .forms import ProductoForm
from .models import Categoria, Producto, Proveedor, Movimiento

from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    CategoriaSerializer,
    ProductoSerializer,
    ReporteProductoSerializer,
    ContactSerializer,
    ProveedorSerializer,
    MovimientoSerializer
)

from .permissions import IsUserAlmacen
from .utils import permission_required

import logging

logger = logging.getLogger(__name__)

# ============================
# Views normales
# ============================

def index(request):
    return HttpResponse("Hola mundo")

def contact(request, name):
    return HttpResponse(f"Hola {name} bienvenido a la clase de Django")

def categorias(request):
    post_nombre = request.POST.get('nombre')
    if post_nombre:
        q = Categoria(nombre=post_nombre)
        q.save()

    filtro_nombre = request.GET.get('nombre')
    if filtro_nombre:
        categorias = Categoria.objects.filter(nombre__contains=filtro_nombre)
    else:
        categorias = Categoria.objects.all()
    return render(request, 'form_categorias.html', {
        "categorias": categorias
    })

def productoFormView(request):
    form = ProductoForm()
    producto = None
    id_producto = request.GET.get('id')
    if id_producto:
        producto = get_object_or_404(Producto, id=id_producto)
        form = ProductoForm(instance=producto)

    if request.method == 'POST':
        if producto:
            form = ProductoForm(request.POST, instance=producto)
        else:
            form = ProductoForm(request.POST)

    if form.is_valid():
        form.save()

    return render(request, 'form_productos.html', {
        "form": form
    })

# ============================
# ModelViewSets y GenericAPIView
# ============================

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsAuthenticated]

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
    permission_classes = [IsAuthenticated]

class CategoriaCreateView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

# ============================
# Custom APIs
# ============================

@api_view(['GET'])
def categoria_count(request):
    try:
        cantidad = Categoria.objects.count()
        return JsonResponse({"cantidad": cantidad}, status=200)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)

@api_view(['GET'])
def producto_en_unidades(request):
    try:
        productos = Producto.objects.filter(unidades="u")
        return JsonResponse(ProductoSerializer(productos, many=True).data, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)

@api_view(['GET'])
@permission_required(["inventario.reporte_cantidad"])
def reporte_productos(request):
    try:
        cantidad = Producto.objects.count()
        productos = Producto.objects.filter(unidades="u")
        logger.info(f"Reporte de productos {cantidad}")
        return JsonResponse(ReporteProductoSerializer({
            "cantidad": cantidad,
            "productos": productos
        }).data, safe=False, status=200)
    except Exception as e:
        logger.error("Se produjo un error")
        return JsonResponse({"message": str(e)}, status=400)

@api_view(['POST'])
def enviar_mensaje(request):
    cs = ContactSerializer(data=request.data)
    if cs.is_valid():
        return JsonResponse({"message": "Mensaje enviado"}, status=200)
    else:
        return JsonResponse({"message": cs.errors}, status=400)

# ============================
# Nueva Custom API: productos disponibles
# ============================

@api_view(['GET'])
def productos_disponibles(request):
    """
    Devuelve todos los productos disponibles (disponible=True)
    """
    productos = Producto.objects.filter(disponible=True)
    return JsonResponse(ProductoSerializer(productos, many=True).data, safe=False, status=200)