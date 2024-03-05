from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date
import datetime
from .helper import helper
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.contrib.auth.models import User




class RegistroForm(UserCreationForm):
    roles = (
                (1, 'Administrador'),
                (2, 'Cliente'),
                (3, 'Empleado'),
                (4, 'Gerente'),
    )
    domicilio = forms.CharField(max_length=255, label="Domicilio")
    telefono = forms.CharField(max_length=15, label="Teléfono")
    
    rol = forms.ChoiceField(choices=roles, label="Tipo de Usuario")
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2', 'rol')
        labels = {
            "first_name": "Nombre y Apellidos", 
        }


class LoginForm(forms.Form):
    usuario = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())





class BusquedaProductoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
class BusquedaAvanzadaProductoForm(forms.Form):
    
    nombre_prod = forms.CharField (required=False, label="Nombre del Producto")
    
    descripcion = forms.CharField (required=False, label="Descripcion del Producto")
    
    precio = forms.DecimalField(required=False)
    
    farmacia_prod = forms.ChoiceField (choices=helper.obtener_farmacias_select(), required=False, label="Farmacia", widget=forms.Select())  
    
    prov_sum_prod = forms.ChoiceField (choices=helper.obtener_proveedores_select(), required=False, label="Proveedor", widget=forms.Select())
    
    
class ProductoForm(forms.Form):
    
    imagen_prod = forms.ImageField()
    
    nombre_prod = forms.CharField(label="Nombre", max_length=200, required=True)
    
    descripcion = forms.CharField(label="Descripcion", required=True, widget=forms.Textarea())

    precio = forms.DecimalField(label="Precio", max_digits=5, decimal_places=2, required=True)

    def __init__(self, *args, **kwargs):
        
        super(ProductoForm, self).__init__(*args, **kwargs)
        
        #OneToOne o ManyToOne (ChoiceField)
        farmaciasDisponibles = helper.obtener_farmacias_select()
        self.fields["farmacia_prod"] = forms.ChoiceField(
            choices = farmaciasDisponibles,
            widget=forms.Select,
            required=True,
        )
        
        #ManyToMany (MultipleChoiceField)
        proveedores_Disponibles = helper.obtener_proveedores_select()
        self.fields["prov_sum_prod"] = forms.MultipleChoiceField(
            choices=proveedores_Disponibles,
            required=True,
            help_text="Mantén pulsada la tecla de control para seleccionar varios elementos."
        )
   
class ProductoActualizarNombreForm(forms.Form):
    nombre_prod = forms.CharField(label="Nombre del Producto",
                                  max_length=200,
                                  required=True,
                                  help_text="200 caracteres como máximo")
   
 
 
 

class BusquedaEmpleadoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
        

class BusquedaAvanzadaEmpleadoForm(forms.Form):
    
    first_name = forms.CharField (required=False, label="Nombre del Empleado")
    
    email = forms.EmailField(required=False, label="Email del Empleado")
    
    date_joined = forms.DateField (required=False, label="Fecha de Registro | dd-mm-yyyy", input_formats=['%d-%m-%Y'], widget=forms.DateInput(attrs={'type': 'date'}))
    
    salario = forms.FloatField(required=False, label="Salario del Empleado")
    
    direccion_emp = forms.CharField(label="Direccion", required=False)
    
    telefono_emp = forms.IntegerField(label="Telefono", required=False)
    
    farm_emp = forms.ChoiceField (choices=helper.obtener_farmacias_select(), required=False, label="Farmacia Asignada", widget=forms.Select())
   
    
"""
class EmpleadoModelForm(UserCreationForm):
    
    email = forms.EmailField(label="Email del empleado")
    
    salario = forms.FloatField(label="Salario", required=True, help_text='Salario del Empleado')
    
    farm_emp = forms.ModelChoiceField (queryset=Farmacia.objects.all(), required=False, label='Farmacia Asignada', widget=forms.Select())
    
    first_name = forms.CharField(label="Nombre y Apellidos", required=True)
    
    direccion_emp = forms.CharField(label="Direccion", required=True)
    
    telefono_emp = forms.IntegerField(label="Telefono", required=True)
    

    def __init__(self, *args, **kwargs):
        
        super(ProductoForm, self).__init__(*args, **kwargs)
        
        #OneToOne o ManyToOne (ChoiceField)
        farmaciasDisponibles = helper.obtener_farmacias_select()
        self.fields["farmacia_prod"] = forms.ChoiceField(
            choices = farmaciasDisponibles,
            widget=forms.Select,
            required=True,
        )
        
        #ManyToMany (MultipleChoiceField)
        proveedores_Disponibles = helper.obtener_proveedores_select()
        self.fields["prov_sum_prod"] = forms.MultipleChoiceField(
            choices=proveedores_Disponibles,
            required=True,
            help_text="Mantén pulsada la tecla de control para seleccionar varios elementos."
        )
   
class EmpleadoActualizarNombreForm(forms.Form):
    first_name = forms.CharField(label="Nombre del Empleado",
                                  max_length=200,
                                  required=True,
                                  help_text="50 caracteres como máximo")
      
"""


class BusquedaFarmaciaForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)

class FarmaciaForm(forms.Form):
    
    nombre_farm = forms.CharField (label="Nombre de la Farmacia", required=True)
    
    direccion_farm = forms.CharField (label="Dirección",required=True)
    
    telefono_farm = forms.IntegerField(label="Teléfono", required=True)
    
class FarmaciaActualizarNombreForm(forms.Form):
    nombre_farm = forms.CharField(label="Nombre",
                                  max_length=200,
                                  required=True,
                                  help_text="200 carácteres como máximo")
   
 



class BusquedaVotacionForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)

class BusquedaAvanzadaVotacionForm(forms.Form):
    puntuacion = forms.IntegerField (required=False, label="Puntuacion")
    
    fecha_desde = forms.DateField(label="Fecha Desde",
                                required=False,
                                widget= forms.SelectDateWidget(years=range(1990,2030))
                                )
    
    fecha_hasta = forms.DateField(label="Fecha Hasta",
                                  required=False,
                                  widget= forms.SelectDateWidget(years=range(1990,2030))
                                )       
    
    comenta_votacion = forms.CharField(required=False)
    
    voto_producto = forms.ChoiceField (choices=helper.obtener_productos_select(), required=False, label="Producto", widget=forms.Select())  
    
    voto_cliente = forms.ChoiceField (choices=helper.obtener_clientes_select(), required=False, label="Cliente", widget=forms.Select())
    

class VotacionForm(forms.Form):
    
    numeros = [
        (1,"1"), 
        (2,"2"), 
        (3,"3"),
        (4,"4"),
        (5,"5"),
        ]
    puntuacion = forms.ChoiceField(choices=numeros, required=True)
    fecha_votacion = forms.DateField(initial=datetime.date.today())
    comenta_votacion = forms.CharField()
    
    def __init__(self, *args, **kwargs):
        
        super(VotacionForm, self).__init__(*args, **kwargs)
        
        productosDisponibles = helper.obtener_productos_select()
        self.fields["voto_producto"] = forms.ChoiceField(
            choices=productosDisponibles,
            widget=forms.Select,
            required=True,
        )
        
        clientesDisponibles = helper.obtener_clientes_select()
        self.fields["voto_cliente"] = forms.ChoiceField(
            choices = clientesDisponibles,
            widget=forms.Select,
            required=True,
        )
    
    
class VotacionActualizarPuntuacionForm(forms.Form):
    
    numeros = [
        (1,"1"), 
        (2,"2"), 
        (3,"3"),
        (4,"4"),
        (5,"5"),
        ]
    puntuacion = forms.ChoiceField(choices=numeros, required=True)
   
 

