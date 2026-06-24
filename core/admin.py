from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Marca, Sucursal, Vendedor, Vehiculo, Cliente, Venta


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'telefono', 'is_staff']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'dni']
    list_filter = ['is_staff', 'is_active', 'groups']
    fieldsets = UserAdmin.fieldsets + (
        ('Datos adicionales', {'fields': ('telefono', 'dni')}),
    )


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'pais_origen']
    search_fields = ['nombre', 'pais_origen']
    list_filter = ['pais_origen']
    ordering = ['nombre']


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ciudad', 'direccion', 'telefono']
    search_fields = ['nombre', 'ciudad', 'direccion']
    list_filter = ['ciudad']
    ordering = ['ciudad', 'nombre']


@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ['legajo', 'usuario', 'sucursal', 'comision_porcentaje']
    search_fields = ['legajo', 'usuario__first_name', 'usuario__last_name']
    list_filter = ['sucursal']
    ordering = ['legajo']


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ['modelo', 'marca', 'anio', 'precio', 'condicion', 'disponible', 'sucursal']
    search_fields = ['modelo', 'marca__nombre', 'color']
    list_filter = ['condicion', 'disponible', 'marca', 'sucursal', 'anio']
    ordering = ['-fecha_ingreso']
    list_editable = ['disponible']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['apellido', 'nombre', 'dni', 'email', 'telefono']
    search_fields = ['apellido', 'nombre', 'dni', 'email']
    ordering = ['apellido', 'nombre']


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['pk', 'vehiculo', 'cliente', 'vendedor', 'fecha', 'precio_final']
    search_fields = ['vehiculo__modelo', 'cliente__apellido', 'vendedor__legajo']
    list_filter = ['fecha', 'vendedor__sucursal']
    ordering = ['-fecha']
    date_hierarchy = 'fecha'
