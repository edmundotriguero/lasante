from django.db import models
# para crear modelos bases para generar herencia futuras
from django.contrib.auth.models import User


#modelos general
class ClaseModelo(models.Model):
    estado = models.BooleanField(default=True)
    f_creacion = models.DateTimeField(auto_now_add=True)
    f_modificacion = models.DateTimeField(auto_now=True)
    user_created = models.ForeignKey(User, on_delete=models.CASCADE)
    user_updated = models.IntegerField(blank=True, null=True)

    class Meta:
        abstract=True


