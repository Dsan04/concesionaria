"""
Ejecutar con: python manage.py shell < setup_inicial.py
Crea superusuario, grupos con permisos y datos de prueba.
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'concesionaria.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Usuario, Marca, Sucursal, Vendedor, Vehiculo, Cliente

# ---- SUPERUSUARIO ----
if not Usuario.objects.filter(username='admin').exists():
    admin = Usuario.objects.create_superuser('admin', 'admin@AutoDel.com', 'admin1234')
    admin.first_name = 'Admin'
    admin.last_name = 'Sistema'
    admin.save()
    print('✅ Superusuario creado: admin / admin1234')
else:
    print('ℹ️  Superusuario ya existe')

# ---- GRUPOS Y PERMISOS ----
def get_perms(model, actions):
    ct = ContentType.objects.get_for_model(model)
    return [Permission.objects.get(codename=f'{a}_{model.__name__.lower()}', content_type=ct) for a in actions]

# Grupo Gerente: todo
gerente, _ = Group.objects.get_or_create(name='Gerente')
for model in [Marca, Sucursal, Vendedor, Vehiculo, Cliente]:
    gerente.permissions.add(*get_perms(model, ['add', 'change', 'delete', 'view']))
print('✅ Grupo Gerente creado')

# Grupo Vendedor: solo clientes y vehiculos (view) + venta (add)
from core.models import Venta
vendedor_group, _ = Group.objects.get_or_create(name='Vendedor')
vendedor_group.permissions.add(*get_perms(Cliente, ['add', 'change', 'view']))
vendedor_group.permissions.add(*get_perms(Vehiculo, ['view']))
vendedor_group.permissions.add(*get_perms(Venta, ['add', 'view']))
print('✅ Grupo Vendedor creado')

# ---- DATOS DE PRUEBA ----
if not Marca.objects.exists():
    toyota = Marca.objects.create(nombre='Toyota', pais_origen='Japón')
    ford = Marca.objects.create(nombre='Ford', pais_origen='Estados Unidos')
    vw = Marca.objects.create(nombre='Volkswagen', pais_origen='Alemania')
    print('✅ Marcas creadas')

    suc1 = Sucursal.objects.create(nombre='Central', direccion='Av. Corrientes 1234', telefono='011-4444-5555', ciudad='Buenos Aires')
    suc2 = Sucursal.objects.create(nombre='Norte', direccion='Av. Libertador 800', telefono='011-3333-2222', ciudad='Buenos Aires')
    print('✅ Sucursales creadas')

    Vehiculo.objects.create(marca=toyota, sucursal=suc1, modelo='Corolla', anio=2023, precio=28000000,
                            kilometraje=0, condicion='nuevo', transmision='automatica', color='Blanco',
                            descripcion='Sedán familiar, excelente rendimiento.', imagen='vehiculos/placeholder.jpg')
    Vehiculo.objects.create(marca=ford, sucursal=suc1, modelo='Ranger', anio=2022, precio=45000000,
                            kilometraje=15000, condicion='usado', transmision='manual', color='Negro',
                            descripcion='Pickup robusta para todo terreno.', imagen='vehiculos/placeholder.jpg')
    Vehiculo.objects.create(marca=vw, sucursal=suc2, modelo='Golf', anio=2024, precio=35000000,
                            kilometraje=0, condicion='nuevo', transmision='automatica', color='Gris',
                            descripcion='Compacto premium con tecnología de punta.', imagen='vehiculos/placeholder.jpg')
    print('✅ Vehículos creados')

    Cliente.objects.create(nombre='Juan', apellido='Pérez', dni='30111222', email='juan@mail.com', telefono='1155667788')
    Cliente.objects.create(nombre='María', apellido='González', dni='28333444', email='maria@mail.com', telefono='1144556677')
    print('✅ Clientes creados')
else:
    print('ℹ️  Datos de prueba ya existen')

print('\n🚀 Setup completo. Iniciá el servidor con: python manage.py runserver')
