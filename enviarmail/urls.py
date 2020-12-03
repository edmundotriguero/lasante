from django.urls import path
from .views import reporte

urlpatterns = [
    # vistas para categorias
    
    path('send', reporte, name='send'),
   


    

]