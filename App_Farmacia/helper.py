import requests
import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

class helper:
    
    def obtener_farmacias_select():
        #obtenemos todos los libros
        headers = {'Authorization': 'Bearer ' +env("TOKEN_ACCESS")}
        response = requests.get('http://127.0.0.1:8000/api/v1/farmacias', headers=headers)
        farmacias = response.json()
        
        lista_farmacias = [("","Ninguna")]
        for farmacia in farmacias:
            
        
        