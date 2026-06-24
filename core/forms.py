from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Vehiculo, Cliente, Marca, Sucursal, Venta, Vendedor

INPUT = {'class': 'form-control'}
SELECT = {'class': 'form-select'}
TEXTAREA = {'class': 'form-control', 'rows': 3}


class RegistroForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, label='Nombre', widget=forms.TextInput(attrs=INPUT))
    last_name = forms.CharField(max_length=100, required=True, label='Apellido', widget=forms.TextInput(attrs=INPUT))
    email = forms.EmailField(required=True, label='Email', widget=forms.EmailInput(attrs=INPUT))

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono', 'dni', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs=INPUT),
            'telefono': forms.TextInput(attrs=INPUT),
            'dni': forms.TextInput(attrs=INPUT),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs=INPUT)
        self.fields['password2'].widget = forms.PasswordInput(attrs=INPUT)


class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['marca', 'sucursal', 'modelo', 'anio', 'precio', 'kilometraje',
                  'condicion', 'transmision', 'color', 'descripcion', 'imagen', 'disponible']
        widgets = {
            'marca': forms.Select(attrs=SELECT),
            'sucursal': forms.Select(attrs=SELECT),
            'modelo': forms.TextInput(attrs=INPUT),
            'anio': forms.NumberInput(attrs=INPUT),
            'precio': forms.NumberInput(attrs=INPUT),
            'kilometraje': forms.NumberInput(attrs=INPUT),
            'condicion': forms.Select(attrs=SELECT),
            'transmision': forms.Select(attrs=SELECT),
            'color': forms.TextInput(attrs=INPUT),
            'descripcion': forms.Textarea(attrs=TEXTAREA),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'dni', 'email', 'telefono', 'direccion']
        widgets = {f: forms.TextInput(attrs=INPUT) for f in ['nombre', 'apellido', 'dni', 'telefono', 'direccion']}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(attrs=INPUT)


class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre', 'pais_origen', 'logo']
        widgets = {
            'nombre': forms.TextInput(attrs=INPUT),
            'pais_origen': forms.TextInput(attrs=INPUT),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
        }


class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = ['nombre', 'direccion', 'telefono', 'ciudad']
        widgets = {f: forms.TextInput(attrs=INPUT) for f in ['nombre', 'direccion', 'telefono', 'ciudad']}


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['vehiculo', 'cliente', 'vendedor', 'precio_final', 'observaciones']
        widgets = {
            'vehiculo': forms.Select(attrs=SELECT),
            'cliente': forms.Select(attrs=SELECT),
            'vendedor': forms.Select(attrs=SELECT),
            'precio_final': forms.NumberInput(attrs=INPUT),
            'observaciones': forms.Textarea(attrs=TEXTAREA),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehiculo'].queryset = Vehiculo.objects.filter(disponible=True)
