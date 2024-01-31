from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('productos/lista/api',views.productos_lista_api, name='lista_productos_api'),
    path('productos/lista/api/mejorado',views.productos_lista_api_mejorado, name='lista_productos_api_mejorado'),
    path('producto/busqueda_simple', views.producto_busqueda_simple, name='producto_busqueda_simple'),
    path('producto/busqueda_avanzada', views.producto_busqueda_avanzada, name='producto_busqueda_avanzada'),
    path('producto/crear', views.producto_crear, name='producto_crear'),
    
    path('empleado/lista/api',views.empleados_lista_api, name='lista_empleados_api'),
    path('empleado/lista/api/mejorado',views.empleados_lista_api_mejorado, name='lista_empleados_api_mejorado'),
    
    path('votacion/lista/api/mejorado',views.votaciones_lista_api_mejorado, name='lista_votaciones_api_mejorado'),
       
]
