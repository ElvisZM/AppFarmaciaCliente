from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('productos/lista/api',views.productos_lista_api, name='lista_productos_api'),
    path('producto/busqueda_simple', views.producto_busqueda_simple, name='producto_busqueda_simple'),
    path('producto/busqueda_avanzada', views.producto_busqueda_avanzada, name='producto_busqueda_avanzada'),
       
]
