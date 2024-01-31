import requests
import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

class helper:
    
    #Funcion para obtener todas las farmacias:
    def obtener_farmacias_select():
        #obtenemos todas las farmacias
        headers = {'Authorization': 'Bearer ' +env("TOKEN_ACCESS")}
        response = requests.get('http://127.0.0.1:8000/api/v1/farmacias', headers=headers)
        farmacias = response.json()
        
        lista_farmacias = [("","Ninguna")]
        for farmacia in farmacias:
            lista_farmacias.append((farmacia["id"], farmacia["nombre_farm"]))
        return lista_farmacias
    
    
    #Funcion para obtener todos los proveedores:
    def obtener_proveedores_select():
        #obtenemos todos los proveedores
        headers = {'Authorization': 'Bearer ' +env("TOKEN_ACCESS")}
        response = requests.get('http://127.0.0.1:8000/api/v1/proveedores', headers=headers)
        proveedores = response.json()
        lista_proveedores = []
        for proveedor in proveedores:
            lista_proveedores.append((proveedor["id"], proveedor["nombre_prov"]))
        return lista_proveedores
            
        
        