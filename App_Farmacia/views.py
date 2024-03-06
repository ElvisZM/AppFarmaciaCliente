from django.shortcuts import render, redirect
from .forms import *
from requests.exceptions import HTTPError
from datetime import datetime as dt, date
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .helper import helper
import json
from django.contrib import messages
import xml.etree.ElementTree as ET



import requests
import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)

def index(request):
    if(not "fecha_inicio" in request.session):
        request.session["fecha_inicio"] = dt.now().strftime("%d/%m/%Y %H:%M")
    return render(request, 'index.html')

def crear_cabecera():
    return {'Authorization': 'Bearer '+ env("TOKEN_ACCESO")}

def crear_cabecera_TOKEN_USUARIO(request):
    TOKEN = request.session["token"]
    return {'Authorization': f'Bearer {TOKEN}', "Content-Type": "application/json"}

def formato_respuesta(response):
    content_type = response.headers.get('Content-Type', '')
    
    if 'application/json' in content_type:
        return response.json()
    
    elif 'application/xml' in content_type:
        xml_data = response.content
        root = ET.fromstring(xml_data)
        return xml_to_dict(root)
    
    elif 'text/html' in content_type:
        return response.text

    else:
        return response.content
    

def xml_to_dict(xml_element):
    data = {}
    for child in xml_element:
        if child.taf in data:
            if isinstance(data[child.tag], list):
                data[child.tag].append(xml_to_dict(child))
            else:
                data[child.tag] = [data[child.tag], xml_to_dict(child)]
        else:
            data[child.tag] = xml_to_dict(child) if len(child) > 0 else child.text
    return data                
                

def registrar_usuario(request):
    if (request.method == "POST"):
        try:
            formulario = RegistroForm(request.POST)
            if(formulario.is_valid()):
                headers =  {
                            "Content-Type": "application/json" 
                        }
                response = requests.post(
                    'http://127.0.0.1:8000/api/v1/registrar/usuario',
                    data=json.dumps(formulario.cleaned_data)
                )
                
                if(response.status_code == requests.codes.ok):
                    usuario = response.json()
                    token_acceso = helper.obtener_token_session(
                            formulario.cleaned_data.get("username"),
                            formulario.cleaned_data.get("password1")
                            )
                    request.session["usuario"]=usuario
                    request.session["token"] = token_acceso
                    return redirect("index")
                else:
                    print(response.status_code)
                    response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'registration/signup.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
            
    else:
        formulario = RegistroForm()
    return render(request, 'registration/signup.html', {'formulario': formulario})



def login_menu(request):
    if (request.method == "POST"):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            token_acceso = helper.obtener_token_session(
                                username,
                                password
                                )
            request.session["token"] = token_acceso
            
          
            headers = {'Authorization': 'Bearer '+ token_acceso} 
            response = requests.get('http://127.0.0.1:8000/api/v1/usuario/token/'+token_acceso,headers=headers)
            usuario = response.json()
            request.session["usuario"] = usuario
            
            print(request.session["token"])
            return  redirect("index")
        except Exception as excepcion:
            print(f'Hubo un error en la petición: {excepcion}')
            formulario.add_error("usuario",excepcion)
            formulario.add_error("password",excepcion)
            return redirect("index")
    else:  
        formulario = LoginForm()
    return render(request, 'registration/login_menu.html', {'form': formulario})


def logout(request):
    del request.session['token']
    return redirect('index')


def productos_lista_api(request):
    headers = crear_cabecera()
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
    headers = crear_cabecera()
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
            messages.success(request, f'Estos son los resultados para: "{formulario.cleaned_data["textoBusqueda"]}".')

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
            print(formulario.data)
                       
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
            headers = crear_cabecera_TOKEN_USUARIO(request)
            datos = formulario.data.copy()
            datos["prov_sum_prod"] = request.POST.getlist("prov_sum_prod");
            imagen = request.FILES["imagen_prod"]
            response = requests.post(env('DIRECCION_BASE') + 'producto/crear', 
                headers=headers,
                data=datos,
                files={"imagen_prod":imagen}
            )
            
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha creado el producto '+datos.get('nombre_prod')+' correctamente.')
                
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
            
def producto_obtener(request, producto_id):
    producto = helper.obtener_producto(producto_id)
    return render(request, 'producto/producto_mostrar.html', {'producto': producto})
    
def producto_editar(request, producto_id):
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
        
    producto = helper.obtener_producto(producto_id)
    formulario = ProductoForm(datosFormulario,
            initial={
                    'nombre_prod': producto['nombre_prod'],
                    'descripcion': producto['descripcion'],
                    'precio': producto['precio'],
                    'farmacia_prod': producto['farmacia_prod']['id'],
                    'prov_sum_prod': [proveedor['id'] for proveedor in producto['prov_sum_prod']]   
            }            
    )
    
    if (request.method == "POST"):
        try:
            formulario = ProductoForm(request.POST)
            headers = crear_cabecera_TOKEN_USUARIO(request)
            datos = request.POST.copy()
            datos["prov_sum_prod"] = request.POST.getlist("prov_sum_prod")
            
            response = requests.put(env('DIRECCION_BASE') + 'producto/editar/'+str(producto_id),
            headers=headers,
            data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha editado el producto '+datos.get('nombre_prod')+' correctamente.')
                
                return redirect("producto_mostrar", producto_id=producto_id)
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
                              'producto/actualizar.html',
                              {"formulario":formulario, "producto":producto})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)

    return render(request, 'producto/actualizar.html',{"formulario":formulario, "producto":producto})
            
    
def producto_editar_nombre(request, producto_id):
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
        
    producto = helper.obtener_producto(producto_id)
    formulario = ProductoActualizarNombreForm(datosFormulario,
                                              initial={
                                                  'nombre_prod': producto['nombre_prod']
                                              })
    if (request.method == "POST"):
        try:
            formulario = ProductoForm(request.POST)
            headers = crear_cabecera_TOKEN_USUARIO(request)
            datos = request.POST.copy()
            response = requests.patch(
                env("DIRECCION_BASE") + 'producto/actualizar/nombre/' +str(producto_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha cambiado el nombre del producto '+datos.get('nombre_prod')+' correctamente.')
                
                return redirect('producto_mostrar',producto_id=producto_id)
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
                              'producto/actualizar_nombre.html',
                              {"formulario":formulario, "producto":producto})
                
            else:
                return mis_errores(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'producto/actualizar_nombre.html', {"formulario":formulario, "producto":producto})


def producto_eliminar(request, producto_id):
    try:
        headers = crear_cabecera_TOKEN_USUARIO(request)
        response = requests.delete(
            env("DIRECCION_BASE") + 'producto/eliminar/'+str(producto_id),
            headers=headers,
        )
        if(response.status_code == requests.codes.ok):
            messages.success(request, 'Se ha eliminado el producto correctamente.')
            
            return redirect("lista_productos_api_mejorado")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect('lista_productos_api_mejorado')
    
    

def empleados_lista_api(request):
    # Obtenemos todos los productos
    headers = crear_cabecera_TOKEN_USUARIO(request)
    response = requests.get(env('DIRECCION_BASE') + 'empleados',headers=headers)
    # Transformamos la respuesta en json
    empleados = formato_respuesta(response)
    return render(request, 'empleado/lista_empleados_api.html', {'empleados': empleados})

def empleados_lista_api_mejorado(request):
    # Obtenemos todos los productos
    headers = crear_cabecera_TOKEN_USUARIO(request)
    response = requests.get(env('DIRECCION_BASE') + 'empleados/mejorado',headers=headers)
    # Transformamos la respuesta en json
    empleados = formato_respuesta(response)
    return render(request, 'empleado/lista_empleados_api_mejorado.html', {'empleados': empleados})

def empleado_busqueda_avanzada(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaEmpleadoForm(request.GET)
        headers = crear_cabecera_TOKEN_USUARIO(request)
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







def farmacias_lista_api(request):
    # Obtenemos todos los productos
    headers = crear_cabecera()
    try:
        response = requests.get(env('DIRECCION_BASE') + 'farmacias',headers=headers)
        response.raise_for_status()  # Lanzará una excepción si la respuesta tiene un código de error HTTP
        # Transformamos la respuesta en json
        farmacias = formato_respuesta(response)
        return render(request, 'farmacia/lista_api_mejorado.html', {'farmacias': farmacias})
    except requests.exceptions.HTTPError as err:
        print(f"Paso este error: {err}")
        error_code = response.status_code
        return mis_errores(request, error_code)
    except Exception as err:
        print(f"Este error ha ocurrido: {err}")
        # Cualquier otra excepción no relacionada con HTTP
        return mi_error_500(request)


def farmacia_busqueda_simple(request):
    formulario = BusquedaFarmaciaForm(request.GET)
    
    if formulario.is_valid():
        headers = crear_cabecera()
        print(headers)
        try:
            response = requests.get(
                env('DIRECCION_BASE') + 'farmacia/busqueda_simple',
                headers=headers,
                params=formulario.cleaned_data
            )
            print(response)
            response.raise_for_status()  # Lanzará una excepción si la respuesta tiene un código de error HTTP
            farmacias = formato_respuesta(response)
            #print(productos)
            messages.success(request, f'Estos son los resultados para: "{formulario.cleaned_data["textoBusqueda"]}".')
            return render(request, 'farmacia/lista_api_mejorado.html',{"farmacias": farmacias})
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


def farmacia_crear(request):
    if (request.method == "POST"):
        try:
            formulario = FarmaciaForm(request.POST)
            headers = crear_cabecera_TOKEN_USUARIO(request)
            datos = formulario.data.copy()
            response = requests.post(env('DIRECCION_BASE') + 'farmacia/crear',
                headers=headers,
                data=json.dumps(datos),
            )
            print(datos)
            
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha creado la farmacia '+datos.get('nombre_farm')+' correctamente.')

                return redirect("lista_farmacias_api_mejorado")
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
                              'farmacia/create_api.html',
                              {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = FarmaciaForm(None)
    return render(request, 'farmacia/create_api.html',{"formulario":formulario})
            
def farmacia_obtener(request, farmacia_id):
    farmacia = helper.obtener_farmacia(farmacia_id)
    return render(request, 'farmacia/farmacia_mostrar.html', {'farmacia': farmacia})
    
def farmacia_editar(request, farmacia_id):
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
        
    farmacia = helper.obtener_farmacia(farmacia_id)
    formulario = FarmaciaForm(datosFormulario,
            initial={
                    'nombre_farm': farmacia['nombre_farm'],
                    'direccion_farm': farmacia['direccion_farm'],
                    'telefono_farm': farmacia['telefono_farm'],
            }            
    )
    
    if (request.method == "POST"):
        try:
            formulario = FarmaciaForm(request.POST)
            headers = crear_cabecera_TOKEN_USUARIO(request)
            datos = request.POST.copy()
            response = requests.put(env('DIRECCION_BASE') + 'farmacia/editar/'+str(farmacia_id),
            headers=headers,
            data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha editado la farmacia '+datos.get('nombre_farm')+' correctamente.')

                return redirect("farmacia_mostrar", farmacia_id=farmacia_id)
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
                              'farmacia/actualizar_farmacia.html',
                              {"formulario":formulario, "farmacia":farmacia})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)

    return render(request, 'farmacia/actualizar_farmacia.html',{"formulario":formulario, "farmacia":farmacia})
            
    
def farmacia_editar_nombre(request, farmacia_id):
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
        
    farmacia = helper.obtener_farmacia(farmacia_id)
    formulario = FarmaciaActualizarNombreForm(datosFormulario,
                                              initial={
                                                  'nombre_farm': farmacia['nombre_farm']
                                              })
    if (request.method == "POST"):
        try:
            formulario = FarmaciaForm(request.POST)
            headers = crear_cabecera_TOKEN_USUARIO(request)
            datos = request.POST.copy()
            response = requests.patch(
                env("DIRECCION_BASE") + 'farmacia/actualizar/nombre/' +str(farmacia_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha cambiado el nombre de la farmacia '+datos.get('nombre_farm')+' correctamente.')

                return redirect('farmacia_mostrar',farmacia_id=farmacia_id)
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
                              'farmacia/actualizar_nombre.html',
                              {"formulario":formulario, "farmacia":farmacia})
                
            else:
                return mis_errores(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'farmacia/actualizar_nombre.html', {"formulario":formulario, "farmacia":farmacia})


def farmacia_eliminar(request, farmacia_id):
    try:
        headers = crear_cabecera_TOKEN_USUARIO(request)
        response = requests.delete(
            env("DIRECCION_BASE") + 'farmacia/eliminar/'+str(farmacia_id),
            headers=headers,
        )
        print(response)
        if(response.status_code == requests.codes.ok):
            farmacia_eliminada = response.json()
            print("farmacia eliminada")
            print(farmacia_eliminada)
            messages.success(request, 'Se ha eliminado la farmacia correctamente.')
            return redirect("lista_farmacias_api_mejorado")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect('lista_farmacias_api_mejorado')
    
    











def votaciones_lista_api_mejorado(request):
    #headers = {'Authorization': 'Bearer ' + env("TOKEN_ACCESO_JsonWebToken")}
    headers = crear_cabecera()
    response = requests.get(env('DIRECCION_BASE') + 'votaciones/mejorado',headers=headers)
    # Transformamos la respuesta en json
    votaciones = formato_respuesta(response)
    return render(request, 'votacion/lista_votaciones_api_mejorado.html', {'votaciones': votaciones})




def votacion_busqueda_simple(request):
    formulario = BusquedaVotacionForm(request.GET)
    
    if formulario.is_valid():
        headers = crear_cabecera()
        try:
            response = requests.get(
                env('DIRECCION_BASE') + 'votacion/busqueda_simple',
                headers=headers,
                params=formulario.cleaned_data
            )
            response.raise_for_status()  # Lanzará una excepción si la respuesta tiene un código de error HTTP
            votaciones = formato_respuesta(response)
            #print(productos)
            messages.success(request, f'Estos son los resultados para: "{formulario.cleaned_data["textoBusqueda"]}".')
            
            return render(request, 'votacion/lista_votaciones_api_mejorado.html',{"votaciones": votaciones})
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



def votacion_crear(request):
    if (request.method == "POST"):
        try:
            formulario = VotacionForm(request.POST)
            headers = crear_cabecera_TOKEN_USUARIO(request)
            datos = formulario.data.copy()
            response = requests.post(env('DIRECCION_BASE') + 'votacion/crear',
                headers=headers,
                data=json.dumps(datos),
            )
            
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha enviado la votacion a '+datos.get('voto_prod')+' correctamente.')
                
                return redirect("lista_votaciones_api_mejorado")
            else:
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = formato_respuesta(response)
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request,
                              'votacion/create_api.html',
                              {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = VotacionForm(None)
    return render(request, 'votacion/create_api.html',{"formulario":formulario})
            
def votacion_obtener(request, votacion_id):
    votacion = helper.obtener_votacion(votacion_id)
    return render(request, 'votacion/votacion_mostrar.html', {'votacion': votacion})
    
def votacion_editar(request, votacion_id):
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
        
    votacion = helper.obtener_votacion(votacion_id)
    formulario = VotacionForm(datosFormulario,
            initial={
                    'puntuacion': votacion['puntuacion'],
                    'fecha_votacion': votacion['fecha_votacion'],
                    'comenta_votacion': votacion['comenta_votacion'],
                    'voto_producto': votacion['voto_producto']['id'],
                    'voto_cliente': votacion['voto_cliente']['id']
            }            
    )
    
    if (request.method == "POST"):
        try:
            formulario = VotacionForm(request.POST)
            headers = crear_cabecera_TOKEN_USUARIO(request)
            datos = request.POST.copy()
            response = requests.put(env('DIRECCION_BASE') + 'votacion/editar/'+str(votacion_id),
            headers=headers,
            data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha editado la votacion correctamente.')
                
                return redirect("votacion_mostrar", votacion_id=votacion_id)
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
                              'votacion/actualizar_votacion.html',
                              {"formulario":formulario, "votacion":votacion})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)

    return render(request, 'votacion/actualizar_votacion.html',{"formulario":formulario, "votacion":votacion})
            
    
def votacion_editar_puntuacion(request, votacion_id):
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
        
    votacion = helper.obtener_votacion(votacion_id)
    formulario = VotacionActualizarPuntuacionForm(datosFormulario,
                                              initial={
                                                  'puntuacion': votacion['puntuacion']
                                              })
    if (request.method == "POST"):
        try:
            formulario = VotacionForm(request.POST)
            headers = crear_cabecera_TOKEN_USUARIO(request)
            datos = request.POST.copy()
            response = requests.patch(
                env("DIRECCION_BASE") + 'votacion/actualizar/puntuacion/' +str(votacion_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha cambiado la puntuacion correctamente.')
                
                return redirect('votacion_mostrar',votacion_id=votacion_id)
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
                              'votacion/actualizar_puntuacion.html',
                              {"formulario":formulario, "votacion":votacion})
                
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'votacion/actualizar_puntuacion.html', {"formulario":formulario, "votacion":votacion})


def votacion_eliminar(request, votacion_id):
    try:
        headers = crear_cabecera_TOKEN_USUARIO(request)
        response = requests.delete(
            env("DIRECCION_BASE") + 'votacion/eliminar/'+str(votacion_id),
            headers=headers,
        )
        if(response.status_code == requests.codes.ok):
            messages.success(request, 'Se ha eliminado la votacion correctamente.')
            return redirect("lista_votaciones_api_mejorado")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect('lista_votaciones_api_mejorado')
    















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

