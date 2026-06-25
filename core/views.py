from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Vehiculo, Cliente, Marca, Sucursal, Venta, Vendedor
from .forms import RegistroForm, VehiculoForm, ClienteForm, MarcaForm, SucursalForm, VentaForm


# ---------- AUTH ----------

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cuenta creada exitosamente.')
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'auth/registro.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ---------- HOME ----------

@login_required
def home(request):
    vehiculos = Vehiculo.objects.filter(disponible=True)[:6]
    return render(request, 'home.html', {'vehiculos': vehiculos})


# ---------- VEHICULOS ----------

@login_required
def vehiculo_list(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'vehiculos/list.html', {'vehiculos': vehiculos})


@login_required
def vehiculo_detail(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    return render(request, 'vehiculos/detail.html', {'vehiculo': vehiculo})


@permission_required('core.add_vehiculo', raise_exception=True)
def vehiculo_create(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehículo creado correctamente.')
            return redirect('vehiculo_list')
    else:
        form = VehiculoForm()
    return render(request, 'vehiculos/form.html', {'form': form, 'titulo': 'Nuevo Vehículo'})


@permission_required('core.change_vehiculo', raise_exception=True)
def vehiculo_update(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        form = VehiculoForm(request.POST, request.FILES, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehículo actualizado.')
            return redirect('vehiculo_list')
    else:
        form = VehiculoForm(instance=vehiculo)
    return render(request, 'vehiculos/form.html', {'form': form, 'titulo': 'Editar Vehículo'})


@permission_required('core.delete_vehiculo', raise_exception=True)
def vehiculo_delete(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        vehiculo.delete()
        messages.success(request, 'Vehículo eliminado.')
        return redirect('vehiculo_list')
    return render(request, 'vehiculos/confirm_delete.html', {'objeto': vehiculo, 'tipo': 'Vehículo'})


# ---------- CLIENTES ----------

@permission_required('core.view_cliente', raise_exception=True)
def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/list.html', {'clientes': clientes})


@permission_required('core.view_cliente', raise_exception=True)
def cliente_detail(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, 'clientes/detail.html', {'cliente': cliente})


@permission_required('core.add_cliente', raise_exception=True)
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado correctamente.')
            return redirect('cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'clientes/form.html', {'form': form, 'titulo': 'Nuevo Cliente'})


@permission_required('core.change_cliente', raise_exception=True)
def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado.')
            return redirect('cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/form.html', {'form': form, 'titulo': 'Editar Cliente'})


@permission_required('core.delete_cliente', raise_exception=True)
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado.')
        return redirect('cliente_list')
    return render(request, 'clientes/confirm_delete.html', {'objeto': cliente, 'tipo': 'Cliente'})


# ---------- MARCAS ----------

@login_required
def marca_list(request):
    marcas = Marca.objects.all()
    return render(request, 'marcas/list.html', {'marcas': marcas})


@permission_required('core.add_marca', raise_exception=True)
def marca_create(request):
    if request.method == 'POST':
        form = MarcaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marca creada.')
            return redirect('marca_list')
    else:
        form = MarcaForm()
    return render(request, 'marcas/form.html', {'form': form, 'titulo': 'Nueva Marca'})


@permission_required('core.change_marca', raise_exception=True)
def marca_update(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    if request.method == 'POST':
        form = MarcaForm(request.POST, request.FILES, instance=marca)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marca actualizada.')
            return redirect('marca_list')
    else:
        form = MarcaForm(instance=marca)
    return render(request, 'marcas/form.html', {'form': form, 'titulo': 'Editar Marca'})


@permission_required('core.delete_marca', raise_exception=True)
def marca_delete(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    if request.method == 'POST':
        marca.delete()
        messages.success(request, 'Marca eliminada.')
        return redirect('marca_list')
    return render(request, 'marcas/confirm_delete.html', {'objeto': marca, 'tipo': 'Marca'})


# ---------- VENTAS ----------

@permission_required('core.view_venta', raise_exception=True)
def venta_list(request):
    ventas = Venta.objects.select_related('vehiculo', 'cliente', 'vendedor').all()
    return render(request, 'ventas/list.html', {'ventas': ventas})


@permission_required('core.add_venta', raise_exception=True)
def venta_create(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Venta registrada correctamente.')
            return redirect('venta_list')
    else:
        form = VentaForm()
    return render(request, 'ventas/form.html', {'form': form, 'titulo': 'Nueva Venta'})


# ---------- SUCURSALES ----------

@login_required
def sucursal_list(request):
    sucursales = Sucursal.objects.all()
    return render(request, 'sucursales/list.html', {'sucursales': sucursales})
