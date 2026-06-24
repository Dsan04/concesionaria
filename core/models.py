from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    telefono = models.CharField(max_length=20, blank=True)
    dni = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.username})'


class Marca(models.Model):
    nombre = models.CharField(max_length=100)
    pais_origen = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='marcas/', blank=True, null=True)

    def vehiculos_disponibles(self):
        return self.vehiculos.filter(disponible=True).count()

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = 'Marcas'


class Sucursal(models.Model):
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nombre} - {self.ciudad}'

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = 'Sucursales'


class Vendedor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='vendedor')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True, related_name='vendedores')
    legajo = models.CharField(max_length=20, unique=True)
    comision_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)

    def __str__(self):
        return f'{self.usuario.get_full_name()} - Legajo {self.legajo}'

    class Meta:
        verbose_name_plural = 'Vendedores'


class Vehiculo(models.Model):
    CONDICION_CHOICES = [
        ('nuevo', 'Nuevo'),
        ('usado', 'Usado'),
    ]
    TRANSMISION_CHOICES = [
        ('manual', 'Manual'),
        ('automatica', 'Automática'),
    ]

    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='vehiculos')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True, related_name='vehiculos')
    modelo = models.CharField(max_length=150)
    anio = models.IntegerField()
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    kilometraje = models.IntegerField(default=0)
    condicion = models.CharField(max_length=10, choices=CONDICION_CHOICES, default='nuevo')
    transmision = models.CharField(max_length=15, choices=TRANSMISION_CHOICES, default='manual')
    color = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='vehiculos/')
    disponible = models.BooleanField(default=True)
    fecha_ingreso = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.marca} {self.modelo} {self.anio}'

    class Meta:
        ordering = ['-fecha_ingreso']
        verbose_name_plural = 'Vehículos'


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=15, unique=True)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.apellido}, {self.nombre} - DNI {self.dni}'

    class Meta:
        ordering = ['apellido', 'nombre']
        verbose_name_plural = 'Clientes'


class Venta(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT, related_name='ventas')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='ventas')
    vendedor = models.ForeignKey(Vendedor, on_delete=models.PROTECT, related_name='ventas')
    fecha = models.DateField(auto_now_add=True)
    precio_final = models.DecimalField(max_digits=12, decimal_places=2)
    observaciones = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.vehiculo.disponible = False
        self.vehiculo.save()

    def __str__(self):
        return f'Venta #{self.pk} - {self.vehiculo} a {self.cliente}'

    class Meta:
        ordering = ['-fecha']
        verbose_name_plural = 'Ventas'
