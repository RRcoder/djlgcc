from django import forms
from .models import ListaPrecios, Clientes

class ListaPreciosForm(forms.ModelForm):
    class Meta:
        model = ListaPrecios
        fields = ['codigo', 'descripcion', 'precio', 'costo']
        widgets = {
        'codigo': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;'}),
        'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        'precio': forms.NumberInput(attrs={'class': 'form-control'}),
        'costo': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigo'].widget.attrs['maxlength'] = '5'  # tengo q forzarlo en el init pq django usa el largo del campo del modelo y no funca poniendolo en attrs


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



class EntregaMercaderiaForm(forms.Form):
    cliente = forms.ModelChoiceField(queryset=Clientes.objects.all(), label="Selecciona un Cliente") 

class EntregaMercaderiaDetForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=ListaPrecios.objects.all().order_by('codigo'), label="Seleccione producto") 
    cantidad = forms.DecimalField() 
    proceso_id = forms.CharField(widget=forms.HiddenInput(),  label="")
    cliente_id = forms.CharField(widget=forms.HiddenInput(),  label="")

class GuardarPedidoForm(forms.Form):
    proceso_id = forms.IntegerField(widget=forms.HiddenInput(),  label="")
    cliente_id = forms.IntegerField(widget=forms.HiddenInput(),  label="")

class ElegirClienteForm(forms.Form):
    cliente = forms.ModelChoiceField(queryset=Clientes.objects.all(), label="Seleccione cliente") 

class IngresarComprobanteForm(forms.Form):
    id_pedido = forms.IntegerField(widget=forms.HiddenInput())

    TIPOS_COMPROBANTE = [
        ('FC', 'Factura'),
        ('ND', 'Nota de Débito'),
        ('NC', 'Nota de Crédito'),
    ]

    FORMULARIOS = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    ]


    fecha = forms.DateField( label='Fecha del comprobante', widget=forms.DateInput(attrs={'type': 'date'}) )
    tipo_comprobante = forms.ChoiceField( choices=TIPOS_COMPROBANTE, label='Tipo de Comprobante' )
    formulario = forms.ChoiceField( choices=FORMULARIOS, label='Tipo (Letra)')
    punto_venta = forms.IntegerField(label='Punto de Venta' )
    numero_comprobante = forms.IntegerField(label='Nro de Comprobante')
    importe_total = forms.DecimalField( label='Importe', max_digits=12, decimal_places=2)
    #iva = forms.DecimalField( label='IVA', max_digits=10, decimal_places=2    )


class InformePedidosForm(forms.Form):
    cliente = forms.ModelChoiceField(queryset=Clientes.objects.all(), required=True, label='Cliente')
    fecha_desde = forms.DateField(widget=forms.SelectDateWidget(years=range(2020, 2031)), required=True, label='Fecha Desde')
    fecha_hasta = forms.DateField(widget=forms.SelectDateWidget(years=range(2020, 2031)), required=True, label='Fecha Hasta')


# este form sirve cuando el pedido ya esta creado y esta pendiente.
class AgregarMercaderiaForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=ListaPrecios.objects.all().order_by('codigo'), label="Seleccione producto") 
    cantidad = forms.DecimalField() 
    item_id = forms.CharField(widget=forms.HiddenInput(),  label="")



