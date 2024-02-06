from django.shortcuts import render, redirect
from .forms import *
from requests.exceptions import HTTPError
from django.contrib import messages
from .helper import helper
import json


import requests
import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)

def index(request):
    return render(request, 'index.html')

def crear_cabecera():
    return {'Authorization': 'Bearer '+ env("TOKEN_ACCESO")}

def crear_cabecera_post():
    return {'Authorization': 'Bearer '+ env("TOKEN_ACCESO"), "Content-Type": "application/json"}

def formato_respuesta(response):
    return response.json()

def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)

#def productos_lista_api(request):
    # Obtenemos todos los productos
    #headers = {'Authorization': 'Bearer SHleaIZhlO8DDpayPQ7pgNiIPu9ZDz'}
#    headers = {'Authorization': 'Bearer ' + env("TOKEN_ACCESO")}
#    print(headers)
#    response = requests.get(env('DIRECCION_BASE') + 'productos',headers=headers)
    # Transformamos la respuesta en json
#    productos = formato_respuesta(response)
#    return render(request, 'producto/lista_api.html', {'productos': productos})

def productos_lista_api(request):
    headers = {'Authorization': 'Bearer ' + env("TOKEN_ACCESO")}
    try:
        response = requests.get(env('DIRECCION_BASE') + 'productos', headers=headers)
        response.raise_for_status()  # Lanzará una excepción si la respuesta tiene un código de error HTTP
        productos = formato_respuesta(response)
        return render(request, 'producto/lista_api.html', {'productos': productos})
    except requests.exceptions.HTTPError as err:
        print(response.status_code)
        if response.status_code == 400:
            # Error de que la solicitud no pudo ser interpretada o estaba mal formada.
            return mi_error_400(request) 
        elif response.status_code == 401:
            # Error de credenciales de auntenticación inválidas.
            return mi_error_401(request) 
        elif response.status_code == 403:
            # Error de permisos de usuario.
            return mi_error_403(request)
        elif response.status_code == 404:
            # Error de recurso no encontrado.
            return mi_error_404(request)
        else:
            # Otros tipos de errores
            return mi_error_500(request)
    except Exception as err:
        # Cualquier otra excepción no relacionada con HTTP
        return mi_error_500(request)

def productos_lista_api_mejorado(request):
    # Obtenemos todos los productos
    #headers = {'Authorization': 'Bearer SHleaIZhlO8DDpayPQ7pgNiIPu9ZDz'}
    headers = {'Authorization': 'Bearer ' + env("TOKEN_ACCESO")}
    try:
        response = requests.get(env('DIRECCION_BASE') + 'productos/mejorado',headers=headers)
        response.raise_for_status()  # Lanzará una excepción si la respuesta tiene un código de error HTTP
        # Transformamos la respuesta en json
        productos = formato_respuesta(response)
        return render(request, 'producto/lista_api_mejorado.html', {'productos': productos})
    except requests.exceptions.HTTPError as err:
        print(response.status_code)
        if response.status_code == 400:
            # Error de que la solicitud no pudo ser interpretada o estaba mal formada.
            return mi_error_400(request) 
        elif response.status_code == 401:
            # Error de credenciales de auntenticación inválidas.
            return mi_error_401(request) 
        elif response.status_code == 403:
            # Error de permisos de usuario.
            return mi_error_403(request)
        elif response.status_code == 404:
            # Error de recurso no encontrado.
            return mi_error_404(request)
        else:
            # Otros tipos de errores
            return mi_error_500(request)
    except Exception as err:
        # Cualquier otra excepción no relacionada con HTTP
        return mi_error_500(request)


def producto_busqueda_simple(request):
    formulario = BusquedaProductoForm(request.GET)
    
    if formulario.is_valid():
        headers = crear_cabecera()
        try:
            response = requests.get(
                env('DIRECCION_BASE') + 'producto/busqueda_simple',
                headers=headers,
                params=formulario.cleaned_data
            )
            response.raise_for_status()  # Lanzará una excepción si la respuesta tiene un código de error HTTP
            productos = formato_respuesta(response)
            #print(productos)
            return render(request, 'producto/lista_api_mejorado.html',{"productos": productos})
        except requests.exceptions.HTTPError as err:
            error_code = response.status_code
            return mis_errores(request, error_code)
        except Exception as err:
            # Cualquier otra excepción no relacionada con HTTP
            return mi_error_500(request)
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")

def producto_busqueda_avanzada(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaProductoForm(request.GET)
        headers = crear_cabecera()
        try:    
            response = requests.get(
                env('DIRECCION_BASE') + 'producto/busqueda_avanzada',
                headers=headers,
                params=formulario.data
            )
            response.raise_for_status()  # Lanzará una excepción si la respuesta tiene un código de error HTTP
            #if(response.status_code == requests.codes.ok):
            productos = formato_respuesta(response)
            return render(request, 'producto/lista_api_mejorado.html',{"productos":productos})
            #else:
            #    print(response.status_code)
            #    response.raise_for_status()
        except HTTPError as http_err:
            error_code = response.status_code
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = formato_respuesta(response)
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request,
                              'producto/busqueda_avanzada_api.html',
                              {"formulario":formulario, "errores": errores}
                              )
            else:
                return mis_errores(request, error_code)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BusquedaAvanzadaProductoForm(None)
    return render(request, 'producto/busqueda_avanzada_api.html', {"formulario":formulario})


def producto_crear(request):
    if (request.method == "POST"):
        try:
            formulario = ProductoForm(request.POST)
            headers = crear_cabecera_post()
            datos = formulario.data.copy()
            datos["prov_sum_prod"] = request.POST.getlist("prov_sum_prod");
            response = requests.post(env('DIRECCION_BASE') + 'producto/crear',
                headers=headers,
                data=json.dumps(datos),
            )
            print(datos)
            
            if(response.status_code == requests.codes.ok):
                return redirect("lista_productos_api_mejorado")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = formato_respuesta(response)
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request,
                              'producto/create_api.html',
                              {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = ProductoForm(None)
    return render(request, 'producto/create_api.html',{"formulario":formulario})
            
            
            

def empleados_lista_api(request):
    # Obtenemos todos los productos
    headers = crear_cabecera()
    response = requests.get(env('DIRECCION_BASE') + 'empleados',headers=headers)
    # Transformamos la respuesta en json
    empleados = formato_respuesta(response)
    return render(request, 'empleado/lista_empleados_api.html', {'empleados': empleados})

def empleados_lista_api_mejorado(request):
    # Obtenemos todos los productos
    headers = crear_cabecera()
    response = requests.get(env('DIRECCION_BASE') + 'empleados/mejorado',headers=headers)
    # Transformamos la respuesta en json
    empleados = formato_respuesta(response)
    return render(request, 'empleado/lista_empleados_api_mejorado.html', {'empleados': empleados})

def empleado_busqueda_avanzada(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaEmpleadoForm(request.GET)
        headers = crear_cabecera()
        try:    
            response = requests.get(
                env('DIRECCION_BASE') + 'empleado/busqueda_avanzada',
                headers=headers,
                params=formulario.data
            )
            response.raise_for_status()  # Lanzará una excepción si la respuesta tiene un código de error HTTP
            #if(response.status_code == requests.codes.ok):
            empleados = formato_respuesta(response)
            return render(request, 'empleado/lista_empleados_api_mejorado.html',{"empleados":empleados})
            #else:
            #    print(response.status_code)
            #    response.raise_for_status()
        except HTTPError as http_err:
            error_code = response.status_code
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = formato_respuesta(response)
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request,
                              'empleado/busqueda_avanzada_api.html',
                              {"formulario":formulario, "errores": errores}
                              )
            else:
                return mis_errores(request, error_code)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BusquedaAvanzadaEmpleadoForm(None)
    return render(request, 'empleado/busqueda_avanzada_api.html', {"formulario":formulario})






def votaciones_lista_api_mejorado(request):
    #headers = {'Authorization': 'Bearer ' + env("TOKEN_ACCESO_JsonWebToken")}
    headers = crear_cabecera()
    response = requests.get(env('DIRECCION_BASE') + 'votaciones/mejorado',headers=headers)
    # Transformamos la respuesta en json
    votaciones = formato_respuesta(response)
    return render(request, 'votacion/lista_votaciones_api_mejorado.html', {'votaciones': votaciones})

def votacion_busqueda_avanzada(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaVotacionForm(request.GET)
        headers = crear_cabecera()
        try:    
            response = requests.get(
                env('DIRECCION_BASE') + 'votacion/busqueda_avanzada',
                headers=headers,
                params=formulario.data
            )
            response.raise_for_status()  # Lanzará una excepción si la respuesta tiene un código de error HTTP
            #if(response.status_code == requests.codes.ok):
            votaciones = formato_respuesta(response)
            return render(request, 'votacion/lista_votaciones_api_mejorado.html',{"votaciones":votaciones})
            #else:
            #    print(response.status_code)
            #    response.raise_for_status()
        except HTTPError as http_err:
            error_code = response.status_code
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = formato_respuesta(response)
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request,
                              'votacion/busqueda_avanzada_api.html',
                              {"formulario":formulario, "errores": errores}
                              )
            else:
                return mis_errores(request, error_code)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BusquedaAvanzadaVotacionForm(None)
    return render(request, 'votacion/busqueda_avanzada_api.html', {"formulario":formulario})




def mis_errores(request, error_code):
    if error_code == 400:
        return render(request, 'errores/400.html',None,None,400)
    elif error_code == 401:
        return render(request, 'errores/401.html',None,None,401)
    elif error_code == 403:
        return render(request, 'errores/403.html',None,None,403)
    elif error_code == 404:
        return render(request, 'errores/404.html',None,None,404)
    else:
        return render(request, 'errores/500.html', None, None,500)
    


def mi_error_400(request, exception=None):
    return render(request, 'errores/400.html',None,None,400)

def mi_error_401(request, exception=None):
    return render(request, 'errores/401.html',None,None,401)

def mi_error_403(request, exception=None):
    return render(request, 'errores/403.html',None,None,403)

def mi_error_404(request, exception=None):
    return render(request, 'errores/404.html',None,None,404)

def mi_error_500(request, exception=None):
    return render(request, 'errores/500.html',None,None,500)

