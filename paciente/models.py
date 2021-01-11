from django.db import models

# Create your models here.
from bases.models import ClaseModelo
from datetime import date

class Genero(ClaseModelo):
    nombre = models.CharField(max_length=50, blank=False, null=False, unique=True)
    
    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.title()
        super(Genero, self).save()

class Ciudad(ClaseModelo):
    nombre = models.CharField(max_length=50, blank=False, null=False, unique=True)

    def __str__(self):
        return '{}'.format(self.nombre)
    
    def save(self):
        self.nombre = self.nombre.title()
        super(Ciudad, self).save()

class Tipo_documento(ClaseModelo):
    nombre = models.CharField(max_length=50, blank=False, null=False, unique=True)
    
    def __str__(self):
        return '{}'.format(self.nombre)
    
    def save(self):
        self.nombre = self.nombre.title()
        super(Tipo_documento, self).save()

class Paciente(ClaseModelo):
    nombres = models.CharField(max_length=50, blank=False, null=False)
    apellidos = models.CharField(max_length=50, blank=False, null=False)
    documento_identificacion = models.CharField(max_length=50, blank=False, null=False, unique=True)
    fecha_nacimiento = models.DateField(blank=False, null=False)
    tipo_documento = models.ForeignKey(Tipo_documento, on_delete=models.CASCADE)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    celular = models.CharField(max_length=30, blank=False, null=False)
    correo = models.CharField(max_length=255, blank=False, null=False, unique=True)

    def __str__(self):
        return '{} {}'.format(self.nombres, self.apellidos)

    def edad(self):
        today = date.today()
        old = self.fecha_nacimiento
        return today.year - old.year - ((today.month, today.day) < (old.month, old.day))

    
        

    def save(self):
        self.nombres = self.nombres.title()
        self.apellidos = self.apellidos.title()
        super(Paciente, self).save()

    class Meta:
        permissions = [('admin_system', 'Permite la visualizacion de la parte administrativa en menu')]

    