from multiprocessing import context
from re import template
from colorama import reinit
from django.shortcuts import render
from django.views import generic
# Create your views here.
# impoertacion para login 

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin

from django.contrib.auth.decorators import login_required, permission_required

from paciente.models import Paciente
from historia.models import Historia
from inventario.models import Item

import datetime
import pytz

# --  ---  ---  ---  --

class SinPrivilegios(LoginRequiredMixin, PermissionRequiredMixin):
    login_url = 'bases:login'
    raise_exception = False
    redirect_field_name = 'redirecto_to'

    def handle_no_permission(self):
        from django.contrib.auth.models import AnonymousUser
        if not self.request.user == AnonymousUser():
            self.login_url='bases:sin_privilegios'
        return HttpResponseRedirect(reverse_lazy(self.login_url))

# -- start method --

@login_required(login_url='/login/')
def home(request):
    template_name = 'bases/home.html'
    contexto= {}

    paciente = Paciente.objects.filter(estado = True).count()
    fecha = datetime.datetime.now()
    
    consultas_hoy = Historia.objects.filter(fecha_proxima=fecha.date(), estado=True).all()
    citas_hoy = Historia.objects.filter(fecha_proxima=fecha.date(), estado=True).count()

    items = Item.objects.filter(estado=True).all()
    obj_item = []
    for i in items:
        if i.cantidad <= i.cantidad_minima:
            objeto = {}
            objeto['item'] = str(i.nombre) + ' ' + str(i.marca.nombre)
            objeto['cantidad'] = i.cantidad
            objeto['cantidad_minima'] = i.cantidad_minima
            objeto['um'] = i.unidad_medida_basica.nombre
            obj_item.append(objeto)

    # products = Product.objects.filter(state=True).all()
    # contracts_money = Contract.objects.filter(state=True, auspice=False).count()
    # contract_auspice = Contract.objects.filter(state=True, auspice=True).count()
    # general_porcentaje = Order.objects.values('product').annotate(total=Sum('porcentage_contract')).order_by('total').filter(state=True)
    # count_maintenance = Maintenance.objects.values('product').annotate(total=Count('product_id')).order_by('total')
    # time_zone = pytz.timezone('America/La_Paz')
    # for item in consultas_hoy:
        # print(item.fecha_proxima)
        # print(time_zone.localize(item.fecha_proxima))
    # print("======+++======")
    # print(consultas_hoy)


   

    contexto = {'paciente':paciente, 'fecha':fecha, 'citas':citas_hoy, 'consultas':consultas_hoy, 'items':obj_item}
    return render(request, template_name, contexto)

#  --  end method --  
# class Home(LoginRequiredMixin, generic.TemplateView):
#     template_name = 'bases/home.html'
#     login_url = 'bases:login'




class HomesinPrivilegios(generic.TemplateView):
    template_name="bases/error_400.html"



@login_required(login_url='/login/')
def Dashboard(request):
    template_name="bases/dashboard.html"

   

    paciente = Paciente.objects.filter(estado = True).count()

    contexto = {'obj1':paciente} 

    return render(request,template_name,contexto)