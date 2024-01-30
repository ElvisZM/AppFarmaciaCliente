from django.shortcuts import render, redirect
from .forms import *
from requests.exceptions import HTTPError


import requests
import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

def index(request):
    return render(request, 'index.html')

def crear_cabecera():
    return {'Authorization': 'Bearer '+ env("TOKEN_ACCESO")}

def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)

def productos_lista_api(request):
    # Obtenemos todos los productos
    #headers = {'Authorization': 'Bearer SHleaIZhlO8DDpayPQ7pgNiIPu9ZDz'}
    headers = {'Authorization': 'Bearer ' + env("TOKEN_ACCESO")}
    response = requests.get('http://127.0.0.1:8000/api/v1/productos',headers=headers)
    # Transformamos la respuesta en json
    productos = response.json()
    return render(request, 'producto/lista_api.html', {'productos': productos})

def productos_lista_api_mejorado(request):
    # Obtenemos todos los productos
    #headers = {'Authorization': 'Bearer SHleaIZhlO8DDpayPQ7pgNiIPu9ZDz'}
    headers = {'Authorization': 'Bearer ' + env("TOKEN_ACCESO")}
    response = requests.get('http://127.0.0.1:8000/api/v1/productos/mejorado',headers=headers)
    # Transformamos la respuesta en json
    productos = response.json()
    return render(request, 'producto/lista_api_mejorado.html', {'productos': productos})

def producto_busqueda_simple(request):
    formulario = BusquedaProductoForm(request.GET)
    
    if formulario.is_valid():
        headers = crear_cabecera()
        response = requests.get(
            'http://127.0.0.1:8000/api/v1/producto/busqueda_simple',
            headers=headers,
            params=formulario.cleaned_data
        )
        productos = response.json()
        #print(productos)
        return render(request, 'producto/lista_api_mejorado.html',{"productos": productos})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
    
def producto_busqueda_avanzada(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaProductoForm(request.GET)
        try:    
            headers = crear_cabecera()
            response = requests.get(
                'http://127.0.0.1:8000/api/v1/producto/busqueda_avanzada',
                headers=headers,
                params=formulario.data
            )
            if(response.status_code == requests.codes.ok):
                productos = response.json()
                return render(request, 'producto/lista_api_mejorado.html',{"productos":productos})
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request,
                              'producto/busqueda_avanzada_api.html',
                              {"formulario":formulario, "errores": errores}
                              )
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BusquedaAvanzadaProductoForm(None)
    return render(request, 'producto/busqueda_avanzada_api.html', {"formulario":formulario})


def empleados_lista_api(request):
    # Obtenemos todos los productos
    headers = crear_cabecera()
    response = requests.get('http://127.0.0.1:8000/api/v1/empleados',headers=headers)
    # Transformamos la respuesta en json
    empleados = response.json()
    return render(request, 'empleado/lista_empleados_api.html', {'empleados': empleados})

def empleados_lista_api_mejorado(request):
    # Obtenemos todos los productos
    headers = crear_cabecera()
    response = requests.get('http://127.0.0.1:8000/api/v1/empleados/mejorado',headers=headers)
    # Transformamos la respuesta en json
    empleados = response.json()
    return render(request, 'empleado/lista_empleados_api_mejorado.html', {'empleados': empleados})

def votaciones_lista_api_mejorado(request):
    #headers = {'Authorization': 'Bearer ' + env("TOKEN_ACCESO_JsonWebToken")}
    headers = crear_cabecera()
    response = requests.get('http://127.0.0.1:8000/api/v1/votaciones/mejorado',headers=headers)
    # Transformamos la respuesta en json
    votaciones = response.json()
    return render(request, 'votacion/lista_votaciones_api_mejorado.html', {'votaciones': votaciones})
