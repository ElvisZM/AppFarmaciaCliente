import requests
import environ
import os
from pathlib import Path
from .views import *

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()

class helper:
    
    
    #Funcion para obtener todas las farmacias:
    def obtener_farmacias_select():
        #obtenemos todas las farmacias
        headers = {'Authorization': 'Bearer ' +env("TOKEN_ACCESO")}
        response = requests.get(env('DIRECCION_BASE') + 'farmacias', headers=headers)
        farmacias = response.json()
        lista_farmacias = [("","Ninguna")]
        for farmacia in farmacias:
            lista_farmacias.append((farmacia["id"], farmacia["nombre_farm"]))
        return lista_farmacias
    
    
    #Funcion para obtener todos los proveedores:
    def obtener_proveedores_select():
        #obtenemos todos los proveedores
        headers = {'Authorization': 'Bearer ' +env("TOKEN_ACCESO")}
        response = requests.get(env('DIRECCION_BASE') + 'proveedores', headers=headers)
        proveedores = response.json()
        lista_proveedores = []
        for proveedor in proveedores:
            lista_proveedores.append((proveedor["id"], proveedor["nombre_prov"]))
        return lista_proveedores
    
    #Funcion para obtener todos los productos
    def obtener_productos_select():
        #obtenemos todos los proveedores
        headers = {'Authorization': 'Bearer ' +env("TOKEN_ACCESO")}
        response = requests.get(env('DIRECCION_BASE') + 'productos', headers=headers)
        productos = response.json()
        lista_productos = [("","")]
        for producto in productos:
            lista_productos.append((producto["id"], producto["nombre_prod"]))
        return lista_productos
    
    #Funcion para obtener todos los clientes
    def obtener_clientes_select():
        #obtenemos todos los proveedores
        headers = {'Authorization': 'Bearer ' +env("TOKEN_ACCESO")}
        response = requests.get(env('DIRECCION_BASE') + 'clientes', headers=headers)
        clientes = response.json()
        lista_clientes = [("","")]
        print(clientes)
        for cliente in clientes:
            usuario = cliente.get("usuario", {})
            nombre_cliente = usuario.get("first_name", f"Cliente {cliente.get('id', '')}")
            lista_clientes.append((cliente.get("id", ""), nombre_cliente))
        return lista_clientes
            
        
    def obtener_producto(id):
        # Obtenemos todos los productos
        headers = {'Authorization': 'Bearer ' +env("TOKEN_ACCESO")}
        response = requests.get(env('DIRECCION_BASE') + 'producto/'+str(id),headers=headers)
        producto = response.json()
        return producto
    
    
    def obtener_farmacia(id):
        #Obtenemos todas las farmacias
        headers = {'Authorization': 'Bearer ' +env("TOKEN_ACCESO")}
        print(headers)
        response = requests.get(env('DIRECCION_BASE') + 'farmacia/'+str(id), headers=headers)
        farmacia = response.json()
        return farmacia
    
    
    def obtener_votacion(id):
        #Obtenemos todas las votaciones
        headers = {'Authorization': 'Bearer ' +env("TOKEN_ACCESO")}
        print(headers)
        response = requests.get(env('DIRECCION_BASE') + 'votacion/'+str(id), headers=headers)
        votacion = response.json()
        return votacion
        
    def obtener_token_session(usuario, password):
        token_url = 'http://127.0.0.1:8000/oauth2/token/'
        data = {
            'grant_type': 'password',
            'username': usuario,
            'password': password,
            'client_id': 'mi_aplicacion',
            'client_secret': 'mi_clave_secreta',
        }
        
        response = requests.post(token_url, data=data)
        
        respuesta = formato_respuesta(response)
        if response.status_code == 200:
            return respuesta.get('access_token')
        else:
            raise Exception(respuesta.get('error_description'))