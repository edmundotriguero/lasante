from django.db import models

# Create your models here.


from bases.models import ClaseModelo


class Marca(ClaseModelo):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    detalle = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.title()

        super(Marca, self).save()


class Unidad_medida(ClaseModelo):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    abreviacion = models.CharField(max_length=50, blank=False, null=False)
    detalle = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.title()

        super(Unidad_medida, self).save()


class Item(ClaseModelo):
    nombre = models.CharField(max_length=50, blank=False, null=False)

    detalle = models.TextField(blank=True, null=True)
    codigo = models.CharField(
        max_length=50, blank=False, null=False, unique=True)
    cantidad = models.FloatField(blank=False, null=False)
    cantidad_minima = models.FloatField(blank=False, null=False)
    cantidad_maxima = models.FloatField(blank=False, null=False)
    unidad_medida_basica = models.ForeignKey(
        Unidad_medida, on_delete=models.CASCADE)
    factor_conversion = models.BooleanField(blank=False)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.title()

        super(Item, self).save()

# um = unidad de medida


class Grupo_um(ClaseModelo):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    um_origen = models.FloatField(blank=False, null=False)

    um_equivalencia = models.FloatField(blank=False, null=False)
    unidad_medida = models.IntegerField(blank=False, null=False)


class Doc_salida(ClaseModelo):
    fecha = models.DateField(blank=False, null=False)
    razon = models.CharField(max_length=110, blank=True, null=True)
    historia_id = models.IntegerField(blank=True, null=True)


class Consumo_inv(ClaseModelo):
    doc_salida = models.ForeignKey(Doc_salida, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cantidad_total = models.FloatField(blank=False, null=False)
    unidad_medida_t = models.ForeignKey(
        Unidad_medida, on_delete=models.CASCADE)
    grupo = models.IntegerField(blank=True, null=True)
    multiplicador = models.FloatField(blank=False, null=False)


class Doc_ingreso(ClaseModelo):
    fecha = models.DateField(blank=False, null=False)
    razon = models.CharField(max_length=110, blank=True, null=True)
    egreso_id = models.IntegerField(blank=True, null=True)


class Detalle_Ingreso(ClaseModelo):
    doc_ingreso = models.ForeignKey(Doc_ingreso, on_delete=models.CASCADE)
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cantidad_total = models.FloatField(blank=False, null=False)
    unidad_medida_t = models.ForeignKey(
        Unidad_medida, on_delete=models.CASCADE)
    grupo = models.IntegerField(blank=True, null=True)
    multiplicador = models.FloatField(blank=False, null=False)
    