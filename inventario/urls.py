from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router para los ViewSets de DRF
router = DefaultRouter()
router.register(r'categorias', views.CategoriaViewSet, basename='categorias')
router.register(r'productos', views.ProductoViewSet, basename='productos')
router.register(r'proveedores', views.ProveedorViewSet, basename='proveedores')

urlpatterns = [
    # Endpoints DRF automáticos
    path('', include(router.urls)),

    # Custom APIs
    path('categorias/cantidad/', views.categoria_count, name='categoria_count'),
    path('productos/filtrar/unidades/', views.producto_en_unidades, name='producto_en_unidades'),
    path('reporte/productos/', views.reporte_productos, name='reporte_productos'),

    # Opcionales: vistas tradicionales con HTML
    path('contact/<str:name>/', views.contact, name='contact'),
    path('categorias/form/', views.categorias, name='categorias_form'),
    path('productos/form/', views.productoFormView, name='producto_form'),
    path('', views.index, name='index'),
]