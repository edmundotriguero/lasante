from django.db import models

from bases.models import ClaseModelo

from paciente.models import Paciente
from medico.models import Medico

from datetime import datetime, timedelta


class Categoria(ClaseModelo):
    nombre = models.CharField(
        max_length=50, blank=False, null=False, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    subcategoria_estado = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.title()
        super(Categoria, self).save()


class Sub_categoria(ClaseModelo):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, blank=False, null=False)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.title()
        super(Sub_categoria, self).save()


# class Carpeta(ClaseModelo):
#     paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, unique=True)
#     expediente = models.CharField(max_length=50, blank=False, null=False)

# TODO: se esta aumentando el campo hora proxima debodo a que django me muestra una fecha en el back end y en la plantilla mee muestra otra fecha ya formateada 
# TODO: Averiguar como se puede obtener esa fecha con otros formatos utc 
class Historia(ClaseModelo):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    sub_categoria = models.TextField(blank=True, null=True)
    proxima_session = models.BooleanField(default=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_proxima = models.DateField(blank=True, null=True)
    hora_proxima = models.TimeField(blank=True, null=True)
    fecha_consulta = models.DateTimeField(blank=False, null=False)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)

    def tiempo_dif(self):
        hoy = datetime.utcnow()
        # print(hoy)
        old = self.fecha_consulta
        print("old")
        dif = ""
        if old:
            hoy = hoy.strftime('%s')
            old = old.strftime('%s')
            
            st = int(hoy) - int(old)
            # print(hoy)

            # print(old)
            # print(st)
            sec = st

            days = int(sec / 86400)
            sec = sec % 86400

            hrs = int(sec / 3600)
            sec = sec % 3600

            mins = int(sec / 60)
            sec =  sec % 60
            dif =  str(days) + " Dias - " + str(hrs) + ":" + str(mins) +":"+ str(sec)
        else:
            dif = "No se tiene registros"
        return dif
