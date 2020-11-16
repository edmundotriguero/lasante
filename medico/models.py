from django.db import models

# Create your models here.
from bases.models import ClaseModelo
from paciente.models import Ciudad, Genero, Tipo_documento

from datetime import date


class Especialidad(ClaseModelo):
    nombre = models.CharField(
        max_length=50, blank=False, null=False, unique=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.title()
        super(Especialidad, self).save()

class Turno(ClaseModelo):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    detalles = models.TextField(blank=True, null=True)
    def __str__(self):
        return '{}'.format(self.nombre)
 
    def save(self):
        self.nombre = self.nombre.title()
        super(Turno, self).save()


class Medico(ClaseModelo):
    nombres = models.CharField(max_length=50, blank=False, null=False)
    apellidos = models.CharField(max_length=50, blank=False, null=False)
    documento_identificacion = models.CharField(
        max_length=50, blank=False, null=False, unique=True)
    tipo_documento = models.ForeignKey(
        Tipo_documento, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField(blank=False, null=False)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    celular = models.CharField(max_length=30, blank=False, null=False)
    correo = models.CharField(
        max_length=255, blank=False, null=False, unique=True)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.nombres, self.apellidos)

    def edad(self):
        today = date.today()
        old = self.fecha_nacimiento
        return today.year - old.year - ((today.month, today.day) < (old.month, old.day))
        

    def save(self):
        self.nombres = self.nombres.title()
        self.apellidos = self.apellidos.title()
        super(Medico, self).save()
