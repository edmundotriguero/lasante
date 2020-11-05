from django.db import models

from bases.models import ClaseModelo

from paciente.models import Paciente


class Categoria(ClaseModelo):
    nombre = models.CharField(max_length=50, blank=False, null=False, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    subcategoria_estado = models.BooleanField(default=True) 

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.title()
        super(Categoria, self).save()

class Sub_categoria(ClaseModelo):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, blank=False, null=False, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.title()
        super(Sub_categoria, self).save()



class Historia(ClaseModelo):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    sub_categoria = models.IntegerField(blank=True, null=True)
    proxima_session = models.BooleanField(default=True)
    descripcion = models.TextField(blank=True, null=True)



