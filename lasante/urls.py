"""lasante URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('',include(('bases.urls','bases'), namespace='bases')),
    
    path('paciente/',include(('paciente.urls','paciente'), namespace='paciente')),
    path('medico/',include(('medico.urls','medico'), namespace='medico')),
    path('enviarmail/',include(('enviarmail.urls','enviarmail'), namespace='enviarmail')),

    path('inventario/',include(('inventario.urls','inventario'), namespace='inventario')),

    path('historia/',include(('historia.urls','historia'), namespace='historia')),
    path('cajas/',include(('cajas.urls','cajas'), namespace='cajas')),
    path('admin/', admin.site.urls),


]
