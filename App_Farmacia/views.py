from django.shortcuts import render, redirect
from .forms import *

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

def productos_lista_api(request):
    # Obtenemos todos los productos
    #headers = {'Authorization': 'Bearer SHleaIZhlO8DDpayPQ7pgNiIPu9ZDz'}
    headers = {'Authorization': 'Bearer ' + env("TOKEN_ACCESO")}
    response = requests.get('http://127.0.0.1:8000/api/v1/productos',headers=headers)
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
    formulario = BusquedaAvanzadaProductoForm(request.GET)
    
    if formulario.is_valid():
        headers = crear_cabecera()
        response = requests.get(
            'http://127.0.0.1:8000/api/v1/producto/busqueda_avanzada',
            headers=headers,
            params=formulario.cleaned_data
        )
        productos = response.json()
        return render(request, 'producto/lista_api_mejorado.html',{"productos":productos})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
    