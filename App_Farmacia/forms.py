from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date
import datetime

class BusquedaProductoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
class BusquedaAvanzadaProductoForm(forms.Form):
    
    nombre_prod = forms.CharField(label="Nombre", max_length=200, required=False)
    
    descripcion = forms.CharField(label="Descripcion", required=False, widget=forms.Textarea())
    
    precio = forms.DecimalField(label="Precio", max_digits=5, decimal_places=2, required=False)
    
    farmacia_prod = forms.ModelChoiceField (queryset=Farmacia.objects.all(), required=False, label="Farmacia", widget=forms.Select())
    
    
    prov_sum_prod = forms.ModelChoiceField (queryset=Proveedor.objects.all(), required=False, label="Proveedor", widget=forms.Select())
    
    
    
        
    