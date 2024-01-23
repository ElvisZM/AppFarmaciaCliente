from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('productos/lista/api',views.productos_lista_api, name='lista_productos_api'),
    path('productos/busqueda_simple', views.producto_busqueda_simple, name='productos_busqueda_simple'),
       
]
