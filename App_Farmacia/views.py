from django.shortcuts import render, redirect

import requests
from django.core import serializers

def index(request):
    return render(request, 'index.html')

def productos_lista_api(request):
    # Obtenemos todos los productos
    response = requests.get('http://127.0.0.1:8000/api/v1/productos')
    # Transformamos la respuesta en json
    productos = response.json()
    return render(request, 'producto/lista_api_cliente.html', {'productos': productos})