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
        fields = ['nombre', 'domicilio_calle', 'domicilio_numero', 'domicilio_piso', 'domicilio_departamento',
        'codigo_postal', 'localidad', 'provincia', 'telefono_fijo', 'telefono_celular', 'email', 'cuit', 
        'tipo' ]
        widgets = {
        'tipo': forms.Select(attrs={'class': 'form-select'}),
        'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.TextInput(attrs={'class': 'form-control'}),
        'cuit': forms.NumberInput(attrs={'class': 'form-control'}),
        'domicilio_calle': forms.TextInput(attrs={'class':'form-control'}),
        'domicilio_numero': forms.TextInput(attrs={'class':'form-control'}),
        'domicilio_piso': forms.TextInput(attrs={'class':'form-control'}),
        'domicilio_departamento': forms.TextInput(attrs={'class':'form-control'}),
        'codigo_postal': forms.TextInput(attrs={'class':'form-control'}),
        'localidad': forms.TextInput(attrs={'class':'form-control'}),
        'provincia': forms.Select(attrs={'class': 'form-select'}),
        'telefono_fijo': forms.TextInput(attrs={'class':'form-control'}),
        'telefono_celular': forms.TextInput(attrs={'class':'form-control'}),
        'email': forms.TextInput(attrs={'class':'form-control'}),
        'cuit': forms.TextInput(attrs={'class':'form-control'}),
        }

class CtaCteForm(forms.ModelForm):
    estado_ctacte= forms.CharField(disabled=True, required=False)

    class Meta:
        model = Clientes
        fields = ['credito' ]
        
class CtaCteBlockForm(forms.ModelForm):
    estado_ctacte = forms.CharField(disabled=True, required=False)
    febaja        = forms.DateField(disabled=True, required=False)

    class Meta:
        model = Clientes
        fields = ['motivobaja' ]



