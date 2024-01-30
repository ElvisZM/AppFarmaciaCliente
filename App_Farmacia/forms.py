from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date
import datetime
from .helper import helper

class BusquedaProductoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
class BusquedaAvanzadaProductoForm(forms.Form):
    
    nombre_prod = forms.CharField(label="Nombre", max_length=200, required=False)
    
    descripcion = forms.CharField(label="Descripcion", required=False, widget=forms.Textarea())
    
    precio = forms.DecimalField(label="Precio", max_digits=5, decimal_places=2, required=False)
    
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
    
        
    