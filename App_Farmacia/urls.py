from django.urls import path
from .import views

urlpatterns = [
    path('login/registrar',views.login_registro, name='login_registro'),
    path('login',views.login, name='login'),
    path('logout', views.logout, name='logout'),
    
    
    path('',views.index,name='index'),
    path('productos/lista/api',views.productos_lista_api, name='lista_productos_api'),
    path('productos/lista/api/mejorado',views.productos_lista_api_mejorado, name='lista_productos_api_mejorado'),
    path('producto/<int:producto_id>',views.producto_obtener, name='producto_mostrar'),
    path('producto/busqueda_simple', views.producto_busqueda_simple, name='producto_busqueda_simple'),
    path('producto/busqueda_avanzada', views.producto_busqueda_avanzada, name='producto_busqueda_avanzada'),
    path('producto/crear', views.producto_crear, name='producto_crear'),
    path('producto/editar/<int:producto_id>', views.producto_editar, name='producto_editar'),
    path('producto/editar/nombre/<int:producto_id>', views.producto_editar_nombre, name='producto_editar_nombre'),
    path('producto/eliminar/<int:producto_id>', views.producto_eliminar, name='producto_eliminar'),
    
    
    path('empleado/lista/api',views.empleados_lista_api, name='lista_empleados_api'),
    path('empleado/lista/api/mejorado',views.empleados_lista_api_mejorado, name='lista_empleados_api_mejorado'),
    path('empleado/busqueda_avanzada', views.empleado_busqueda_avanzada, name='empleado_busqueda_avanzada'),

    
    path('farmacia/lista/api/mejorado', views.farmacias_lista_api, name='lista_farmacias_api_mejorado'),
    path('farmacia/<int:farmacia_id>',views.farmacia_obtener, name='farmacia_mostrar'),
    path('farmacia/busqueda_simple', views.farmacia_busqueda_simple, name='farmacia_busqueda_simple'),
    path('farmacia/crear', views.farmacia_crear, name='farmacia_crear'),
    path('farmacia/editar/<int:farmacia_id>', views.farmacia_editar, name='farmacia_editar'),
    path('farmacia/editar/nombre/<int:farmacia_id>', views.farmacia_editar_nombre, name='farmacia_editar_nombre'),
    path('farmacia/eliminar/<int:farmacia_id>', views.farmacia_eliminar, name='farmacia_eliminar'),
    
    
    
    
    path('votacion/lista/api/mejorado',views.votaciones_lista_api_mejorado, name='lista_votaciones_api_mejorado'),
    path('votacion/<int:votacion_id>',views.votacion_obtener, name='votacion_mostrar'),
    path('votacion/busqueda_avanzada', views.votacion_busqueda_avanzada, name='votacion_busqueda_avanzada'),
    path('votacion/busqueda_simple', views.votacion_busqueda_simple, name='votacion_busqueda_simple'),
    path('votacion/crear', views.votacion_crear, name='votacion_crear'),
    path('votacion/editar/<int:votacion_id>', views.votacion_editar, name='votacion_editar'),
    path('votacion/editar/nombre/<int:votacion_id>', views.votacion_editar_puntuacion, name='votacion_editar_puntuacion'),
    path('votacion/eliminar/<int:votacion_id>', views.votacion_eliminar, name='votacion_eliminar'),
       
       
    path('cliente/lista/api/mejorado',views.clientes_lista, name='lista_clientes_api_mejorado'),
   
       
    path('promocion/lista/api/mejorado',views.promociones_lista, name='lista_promociones_api_mejorado'),
    
    path('clientes/promocion/birthday', views.clientes_lista_promo_cumple, name='clientes_promocion_birthday'),
    
    path('productos/stock/asc', views.filtro_productos_stock_asc, name='filtro_productos_stock_asc'),    
    path('productos/stock/desc', views.filtro_productos_stock_desc, name='filtro_productos_stock_desc'),
    
    path('producto/agregar/carrito/<int:producto_id>', views.agregar_al_carrito, name='agregar_carrito'),
    path('producto/quitar/carrito/<int:producto_id>', views.quitar_del_carrito, name='quitar_del_carrito'),
    path('producto/quitar/unidad/carrito/<int:producto_id>', views.bajar_unidad_carrito, name='bajar_unidad_carrito'),

    path('producto/carrito/usuario', views.carrito_usuario, name="productos_carrito_usuario"),
   
    path('producto/prospecto/<int:producto_id>', views.producto_prospecto, name='producto_prospecto'),
   
    path('tratamientos/lista/mejorada', views.tratamiento_lista_mejorada, name="tratamiento_lista_mejorada"),
   
    path('tratamiento/eliminar/<int:tratamiento_id>', views.tratamiento_eliminar, name="tratamiento_eliminar"),
    
    path('tratamiento/crear', views.tratamiento_crear, name="tratamiento_crear"),


]

handler400 = 'App_Farmacia.views.mi_error_400'
handler403 = 'App_Farmacia.views.mi_error_403'
handler404 = 'App_Farmacia.views.mi_error_404'
handler500 = 'App_Farmacia.views.mi_error_500'