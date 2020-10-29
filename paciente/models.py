from django.db import models

# Create your models here.
from bases.models import ClaseModelo


class Genero(ClaseModelo):
    nombre = models.CharField(max_length=50, blank=False, null=False, unique=True)
    
    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.capitalize()
        super(Genero, self).save()

class Ciudad(ClaseModelo):
    nombre = models.CharField(max_length=50, blank=False, null=False, unique=True)


    def __str__(self):
        return '{}'.format(self.nombre)
    

    def save(self):
        self.nombre = self.nombre.capitalize()
        super(Ciudad, self).save()

class Paciente(ClaseModelo):
    nombres = models.CharField(max_length=50, blank=False, null=False)
    apellidos = models.CharField(max_length=50, blank=False, null=False)
    documento_identificacion = models.CharField(max_length=50, blank=False, null=False, unique=True)
    fecha_nacimiento = models.DateField(blank=False, null=False)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    celular = models.CharField(max_length=30, blank=False, null=False)
    correo = models.CharField(max_length=255, blank=False, null=False, unique=True)


    def __str__(self):
        return '{} {}'.format(self.nombres, self.apellidos)

    def save(self):
        self.nombres = self.nombres.capitalize()
        self.apellidos = self.apellidos.capitalize()
        super(Paciente, self).save()

    