from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('productos/lista/api',views.productos_lista_api, name='lista_productos_api'),
       
]
