from django import forms
from .models import ListaPrecios, Clientes

class ListaPreciosForm(forms.ModelForm):
    class Meta:
        model = ListaPrecios
        fields = ['codigo', 'descripcion', 'precio', 'costo']
        widgets = {
        'codigo': forms.TextInput(attrs={'class': 'form-control'}),
        'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        'precio': forms.NumberInput(attrs={'class': 'form-control'}),
        'costo': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ClientesForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ['nombre', 'email', 'cuit']
        widgets = {
        'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.TextInput(attrs={'class': 'form-control'}),
        'cuit': forms.NumberInput(attrs={'class': 'form-control'}),
        }





