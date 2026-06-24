from .models import Vehiculo, Venta, Cliente


def menu_context(request):
    context = {
        'total_vehiculos_disponibles': Vehiculo.objects.filter(disponible=True).count(),
    }
    if request.user.is_authenticated:
        context['total_ventas'] = Venta.objects.count()
        context['total_clientes'] = Cliente.objects.count()
    return context
