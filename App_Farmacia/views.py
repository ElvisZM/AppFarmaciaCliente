from django.shortcuts import render, redirect
from .forms import *

import requests
import environ
import os
from pathlib import Path



import requests
from django.core import serializers

def index(request):
    return render(request, 'index.html')

def crear_cabecera():
    return {'Authorization': 'Bearer '+env("TOKEN_ACCESO")}

def productos_lista_api(request):
    # Obtenemos todos los productos
    headers = {'Authorization': 'Bearer SHleaIZhlO8DDpayPQ7pgNiIPu9ZDz'}
    response = requests.get('http://127.0.0.1:8000/api/v1/productos',headers=headers)
    # Transformamos la respuesta en json
    productos = response.json()
    return render(request, 'producto/lista_api_mejorado.html', {'productos': productos})

def producto_busqueda_simple(request):
    formulario = BusquedaProductoForm(request.GET)
    
    if formulario.is_valid():
        headers = crear_cabecera()
        response = request.get