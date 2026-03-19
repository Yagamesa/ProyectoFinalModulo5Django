from django.urls import path, include

from . import views

# from rest_framework.routers import DefaultRouter
#
# router = DefaultRouter()
# router.register(r'categorias', views.CategoriaViewSet)

urlpatterns = [
    # path('contact/<str:name>', views.contact),
    # path('categorias', views.categorias, name="categorias"),
    # path('productos', views.productoFormView),
    # path(
    #     'clase8',  views.index
    # )
    # path('', include(router.urls)),
    # path('categoria', views.CategoriaViewSet.as_view({'get': 'list'})),
    path('categorias/cantidad', views.categoria_count),
    path('productos/filtrar/unidades', views.producto_en_unidades),
    path('reporte/productos', views.reporte_productos),
    path('enviar/mensaje', views.enviar_mensaje),
]

