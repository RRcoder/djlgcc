from django import forms
from .models import ListaPrecios

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

