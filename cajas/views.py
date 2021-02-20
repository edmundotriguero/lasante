from django.shortcuts import render, redirect

from django.views import generic
from django.urls import reverse_lazy


from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
import json
from datetime import datetime

from .models import Ingresos, Egresos, Tipo_pago
from .forms import TipopagoForm, IngresoForm, EgresoForm


from paciente.models import Paciente
from medico.models import Medico

#  Clases para Tipo tipo de pago 
class TipopagoView(LoginRequiredMixin, generic.ListView):
    model = Tipo_pago
    template_name = 'tipopago/tipopago_list.html'
    context_object_name = 'obj'
    login_url = 'bases:login'

class TipopagoNew(LoginRequiredMixin, generic.CreateView):
    model = Tipo_pago
    template_name = 'tipopago/tipopago_form.html'
    context_object_name = 'obj'
    form_class = TipopagoForm  
    success_url = reverse_lazy('cajas:tipopago_list')
    login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.user_created = self.request.user

        return super().form_valid(form)

class TipopagoEdit(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Tipo_pago
    template_name = 'tipopago/tipopago_form.html'
    context_object_name = 'obj'
    form_class = TipopagoForm
    success_url = reverse_lazy('cajas:tipopago_list')
    login_url = 'bases:login'
    success_message = "Actializado satisfactoriamente"

    def form_valid(self, form):
        form.instance.user_updated = self.request.user.id

        return super().form_valid(form)


# @login_required(login_url='/login/')
# @permission_required('paciente.delete_genero', login_url='bases:sin_privilegios')
def tipopago_disabled(request, id):
    template_name = 'tipopago/tipopago_disabled.html'
    contexto = {}
    obj = Tipo_pago.objects.get(pk=id)
    if not obj:
        return HttpResponse('Registro no existe' + str(id))

    if request.method == 'GET':
        contexto = {'obj': obj}

    if request.method == 'POST':
        obj.estado = False
        obj.save()
        # mensaje par que la vista lo muestre sin coloca en comentarios pues al momento de los esta haciendo con ajax
        # messages.success(request, 'Se inactivo correctamente')

        contexto = {'obj': 'OK'}
        return HttpResponse('Registro inactivo')

    return render(request, template_name, contexto)


# Clases para Ingresos

def ingreso_view(request):
    
    template_name = 'ingreso/ingreso_list.html'
    contexto = 'obj'
    obj = Ingresos.objects.all()

    inicio = request.GET.get('inicio')
    final = request.GET.get('final')
    print(inicio)
    print(type(inicio))
    if inicio:
        obj = Ingresos.objects.filter(fecha__range = (inicio, final))

    if request.method == 'GET':
        contexto = {'obj': obj}

    if request.method == 'POST':
        
        # obj = Ingresos.objects
        contexto = {'obj': obj}

    return render(request, template_name, contexto)



# ----------

def ingreso_new(request, id):
    template_name = 'ingreso/ingreso_new.html'
    contexto = {}
    obj = Paciente.objects.get(pk=id)
    pago = Tipo_pago.objects.filter(estado=True).all()
    


    if not obj:
        return HttpResponse('Registro no encontrado ' + str(id))

    if request.method == 'GET':
        contexto = {'paciente': obj, 'pago':pago}

    if request.method == 'POST':
        id_paciente = request.POST.get('id_paciente')
        monto = request.POST.get('monto')
        descripcion = request.POST.get('descripcion')
        fecha = request.POST.get('fecha_consulta')
        tipopago = request.POST.get('tipopago')
        
       
        # fecha = datetime.strptime(fecha, "%d/%m/%Y")
        
        

        obj = Ingresos(
            paciente_id=id_paciente,
            detalle=descripcion,
            fecha=fecha,
            monto=monto,
            estado=True,
            tipo_pago_id=tipopago,
            user_created=request.user

        )
        obj.save()
        # return HttpResponse('Reegistro Inactivo !!!')
        return redirect("paciente:paciente_list")

    return render(request, template_name, contexto)


class IngresoEdit(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Ingresos
    template_name = 'ingreso/ingreso_form.html'
    context_object_name = 'obj'
    form_class = IngresoForm
    success_url = reverse_lazy('cajas:ingreso_list')
    login_url = 'bases:login'
    success_message = "Actializado satisfactoriamente"

    def form_valid(self, form):
        form.instance.user_updated = self.request.user.id

        return super().form_valid(form)


# @login_required(login_url='/login/')
# @permission_required('paciente.delete_genero', login_url='bases:sin_privilegios')
def ingreso_disabled(request, id):
    template_name = 'ingreso/ingreso_disabled.html'
    contexto = {}
    obj = Ingresos.objects.get(pk=id)
    if not obj:
        return HttpResponse('Registro no existe' + str(id))

    if request.method == 'GET':
        contexto = {'obj': obj}

    if request.method == 'POST':
        obj.estado = False
        obj.save()
        # mensaje par que la vista lo muestre sin coloca en comentarios pues al momento de los esta haciendo con ajax
        # messages.success(request, 'Se inactivo correctamente')

        contexto = {'obj': 'OK'}
        return HttpResponse('Registro inactivo')

    return render(request, template_name, contexto)



def ingreso_print(request, id):
    template_name = 'ingreso/ingreso_print.html'
    contexto = {}
    obj = Ingresos.objects.get(pk=id)
    
    today = obj.fecha
    year = obj.fecha.year

    # print(year)
    if not obj:
        return HttpResponse('Registro no encontrado ' + str(id))

    if request.method == 'GET':
        contexto = {'obj': obj, 'today':today, 'year':year}

   

    return render(request, template_name, contexto)





# Clases para Egresos

def egreso_view(request):
    
    template_name = 'egreso/egreso_list.html'
    contexto = 'obj'
    obj = Egresos.objects.all()

    inicio = request.GET.get('inicio')
    final = request.GET.get('final')
    print(inicio)
    print(type(inicio))
    if inicio:
        obj = Egresos.objects.filter(fecha__range = (inicio, final))

    if request.method == 'GET':
        contexto = {'obj': obj}

    # if request.method == 'POST':
        
    #     # obj = Ingresos.objects
    #     contexto = {'obj': obj}

    return render(request, template_name, contexto)



# ----------

# class EgresoView(LoginRequiredMixin, generic.ListView):
#     model = Egresos
#     template_name = 'egreso/egreso_list.html'
#     context_object_name = 'obj'
#     login_url = 'bases:login'

# def ingreso_new(request, id):
#     template_name = 'ingreso/ingreso_new.html'
#     contexto = {}
#     obj = Paciente.objects.get(pk=id)
#     pago = Tipo_pago.objects.filter(estado=True).all()
    


#     if not obj:
#         return HttpResponse('Registro no encontrado ' + str(id))

#     if request.method == 'GET':
#         contexto = {'paciente': obj, 'pago':pago}

#     if request.method == 'POST':
#         id_paciente = request.POST.get('id_paciente')
#         monto = request.POST.get('monto')
#         descripcion = request.POST.get('descripcion')
#         fecha = request.POST.get('fecha_consulta')
#         tipopago = request.POST.get('tipopago')
        
       
#         fecha = datetime.strptime(fecha, "%d/%m/%Y %H:%M:%S")
        
        

#         obj = Ingresos(
#             paciente_id=id_paciente,
#             detalle=descripcion,
#             fecha=fecha,
#             monto=monto,
#             estado=True,
#             tipo_pago_id=tipopago,
#             user_created=request.user

#         )
#         obj.save()
#         # return HttpResponse('Reegistro Inactivo !!!')
#         return redirect("paciente:paciente_list")

#     return render(request, template_name, contexto)


class EgresoNew(LoginRequiredMixin, generic.CreateView):
    model = Egresos
    template_name = 'egreso/egreso_form.html'
    context_object_name = 'obj'
    form_class = EgresoForm  
    success_url = reverse_lazy('cajas:egreso_list')
    login_url = 'bases:login'

    # def get_context_data(self, **kwargs):


    def form_valid(self, form):
        fecha = self.request.POST.get('fecha')
        fecha = datetime.strptime(fecha, "%d/%m/%Y")
        form.instance.fecha = fecha
        form.instance.user_created = self.request.user

        return super().form_valid(form)

class EgresoEdit(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Egresos
    template_name = 'egreso/egreso_form.html'
    context_object_name = 'obj'
    form_class = EgresoForm
    success_url = reverse_lazy('cajas:egreso_list')
    login_url = 'bases:login'
    success_message = "Actializado satisfactoriamente"

    def form_valid(self, form):
        form.instance.user_updated = self.request.user.id

        return super().form_valid(form)


# @login_required(login_url='/login/')
# @permission_required('paciente.delete_genero', login_url='bases:sin_privilegios')
def egreso_disabled(request, id):
    template_name = 'egreso/egreso_disabled.html'
    contexto = {}
    obj = Egresos.objects.get(pk=id)
    if not obj:
        return HttpResponse('Registro no existe' + str(id))

    if request.method == 'GET':
        contexto = {'obj': obj}

    if request.method == 'POST':
        obj.estado = False
        obj.save()
        # mensaje par que la vista lo muestre sin coloca en comentarios pues al momento de los esta haciendo con ajax
        # messages.success(request, 'Se inactivo correctamente')

        contexto = {'obj': 'OK'}
        return HttpResponse('Registro inactivo')

    return render(request, template_name, contexto)



def egreso_print(request, id):
    template_name = 'egreso/egreso_print.html'
    contexto = {}
    obj = Egresos.objects.get(pk=id)
    
    today = obj.fecha
    year = obj.fecha.year


    if not obj:
        return HttpResponse('Registro no encontrado ' + str(id))

    if request.method == 'GET':
        contexto = {'obj': obj, 'today':today, 'year':year}

   

    return render(request, template_name, contexto)