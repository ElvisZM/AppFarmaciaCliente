from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date
import datetime
from .helper import helper

class BusquedaProductoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
class BusquedaAvanzadaProductoForm(forms.Form):
    
    nombre_prod = forms.CharField (required=False, label="Nombre del Producto")
    
    descripcion = forms.CharField (required=False)
    
    precio = forms.DecimalField(required=False)
    
    farmacia_prod = forms.ChoiceField (choices=helper.obtener_farmacias_select(), required=False, label="Farmacia", widget=forms.Select())  
    
    prov_sum_prod = forms.ChoiceField (choices=helper.obtener_proveedores_select(), required=False, label="Proveedor", widget=forms.Select())
    
    
class ProductoForm(forms.Form):
    
    nombre_prod = forms.CharField(label="Nombre", max_length=200, required=False)
    
    descripcion = forms.CharField(label="Descripcion", required=False, widget=forms.Textarea())

    precio = forms.DecimalField(label="Precio", max_digits=5, decimal_places=2, required=False)

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
    
        

class BusquedaAvanzadaEmpleadoForm(forms.Form):
    
    first_name = forms.CharField (required=False, label="Nombre del Empleado")
    
    email = forms.EmailField(required=False, label="Email del Empleado")
    
    date_joined = forms.DateField (required=False, label="Fecha de Registro | dd-mm-yyyy", input_formats=['%d-%m-%Y'], widget=forms.DateInput(attrs={'type': 'date'}))
    
    salario = forms.FloatField(required=False, label="Salario del Empleado")
    
    direccion_emp = forms.CharField(label="Direccion", required=False)
    
    telefono_emp = forms.IntegerField(label="Telefono", required=False)
    
    farm_emp = forms.ChoiceField (choices=helper.obtener_farmacias_select(), required=False, label="Farmacia Asignada", widget=forms.Select())
    
      


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
    