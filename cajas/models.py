from django.db import models

from bases.models import ClaseModelo
# Create your models here.
from paciente.models import Paciente


class Tipo_pago(ClaseModelo):
    nombre = models.CharField(max_length=50, null=False, blank=False, unique=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.title()
        super(Tipo_pago, self).save()



class Ingresos(ClaseModelo):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    monto = models.FloatField(blank=False, null=False)
    detalle = models.TextField(blank=True, null=True)
    fecha = models.DateField(blank=False, null=False)
    tipo_pago = models.ForeignKey(Tipo_pago, on_delete=models.CASCADE)


class Egresos(ClaseModelo):
    monto = models.FloatField(blank=False, null=False)
    detalle = models.TextField(blank=True, null=True)
    fecha = models.DateField(blank=False, null=False)
    num_factura = models.CharField(max_length=100,  blank=False, null=False)
    tipo_pago = models.ForeignKey(Tipo_pago, on_delete=models.CASCADE)
