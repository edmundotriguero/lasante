from django.shortcuts import render

from django.views import generic
from django.urls import reverse_lazy


from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required

import json
from datetime import datetime, timedelta

import paciente

from .models import Genero, Ciudad, Tipo_documento, Paciente
from .forms import GeneroForm, CiudadForm, DocumentoForm, PacienteForm

from historia.models import Historia, Categoria, Sub_categoria

from django.db.models import Q, F

from cajas.models import Ingresos

#  Clases para Genero
class GeneroView(LoginRequiredMixin, generic.ListView):
    model = Genero
    template_name = 'genero/genero_list.html'
    context_object_name = 'obj'
    login_url = 'bases:login'

class GeneroNew(LoginRequiredMixin, generic.CreateView):
    model = Genero
    template_name = 'genero/genero_form.html'
    context_object_name = 'obj'
    form_class = GeneroForm  
    success_url = reverse_lazy('paciente:genero_list')
    login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.user_created = self.request.user

        return super().form_valid(form)

class GeneroEdit(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Genero
    template_name = 'genero/genero_form.html'
    context_object_name = 'obj'
    form_class = GeneroForm
    success_url = reverse_lazy('paciente:genero_list')
    login_url = 'bases:login'
    success_message = "Actializado satisfactoriamente"

    def form_valid(self, form):
        form.instance.user_updated = self.request.user.id

        return super().form_valid(form)


# @login_required(login_url='/login/')
# @permission_required('paciente.delete_genero', login_url='bases:sin_privilegios')
def genero_disabled(request, id):
    template_name = 'genero/genero_disabled.html'
    contexto = {}
    obj = Genero.objects.filter(pk=id).first()

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



#  Clases para Ciudad
class CiudadView(LoginRequiredMixin, generic.ListView):
    model = Ciudad
    template_name = 'ciudad/ciudad_list.html'
    context_object_name = 'obj'
    login_url = 'bases:login'

class CiudadNew(LoginRequiredMixin, generic.CreateView):
    model = Ciudad
    template_name = 'ciudad/ciudad_form.html'
    context_object_name = 'obj'
    form_class = CiudadForm  
    success_url = reverse_lazy('paciente:ciudad_list')
    login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.user_created = self.request.user

        return super().form_valid(form)

class CiudadEdit(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Ciudad
    template_name = 'ciudad/ciudad_form.html'
    context_object_name = 'obj'
    form_class = CiudadForm
    success_url = reverse_lazy('paciente:ciudad_list')
    login_url = 'bases:login'
    success_message = "Actializado satisfactoriamente"

    def form_valid(self, form):
        form.instance.user_updated = self.request.user.id

        return super().form_valid(form)


# @login_required(login_url='/login/')
# @permission_required('paciente.delete_genero', login_url='bases:sin_privilegios')
def ciudad_disabled(request, id):
    template_name = 'ciudad/ciudad_disabled.html'
    contexto = {}
    obj = Ciudad.objects.filter(pk=id).first()

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



#  Clases para Tipo Documento 
class DocumentoView(LoginRequiredMixin, generic.ListView):
    model = Tipo_documento
    template_name = 'documento/documento_list.html'
    context_object_name = 'obj'
    login_url = 'bases:login'

class DocumentoNew(LoginRequiredMixin, generic.CreateView):
    model = Tipo_documento
    template_name = 'documento/documento_form.html'
    context_object_name = 'obj'
    form_class = DocumentoForm  
    success_url = reverse_lazy('paciente:documento_list')
    login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.user_created = self.request.user

        return super().form_valid(form)

class DocumentoEdit(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Tipo_documento
    template_name = 'documento/documento_form.html'
    context_object_name = 'obj'
    form_class = DocumentoForm
    success_url = reverse_lazy('paciente:documento_list')
    login_url = 'bases:login'
    success_message = "Actializado satisfactoriamente"

    def form_valid(self, form):
        form.instance.user_updated = self.request.user.id

        return super().form_valid(form)


# @login_required(login_url='/login/')
# @permission_required('paciente.delete_genero', login_url='bases:sin_privilegios')
def documento_disabled(request, id):
    template_name = 'documento/documento_disabled.html'
    contexto = {}
    obj = Tipo_documento.objects.filter(pk=id).first()

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



#  Clases para Tipo Paciente 
class PacienteView(LoginRequiredMixin, generic.ListView):
    model = Paciente
    template_name = 'paciente/paciente_list.html'
    #context_object_name = 'obj'
    login_url = 'bases:login'
    
    def get_queryset(self):      
        return self.model.objects.filter( Q(nombres__icontains=self.request.GET.get('filtro')) | Q(apellidos__icontains=self.request.GET.get('filtro') )| Q(celular__icontains=self.request.GET.get('filtro')) | Q(correo__icontains=self.request.GET.get('filtro')), estado=True).order_by(f'{self.request.GET.get("order_by")}')

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            #TODO: html_action mejorar para estos botones sean consumidos en front, se coloca aqui como solucion temporal por que no se pudo hacer funciona el columnDefs de dataTable
            html_action = "<button class='btn btn-sm btn-outline-success btn-circle btn_add' ><i class='fas fa-file-medical-alt'></i> Add</button>"
            html_action = html_action + "<button class='btn btn-sm btn-outline-info btn-circle btn_ver' ><i class='fas fa-file-medical-alt'></i> Ver</button>"

            html_action1 = "<button class='btn btn-sm btn-outline-success btn-circle btnImprimir' ><i class='fas fa-info'></i></button>"
            html_action1 = html_action1 +  "<button class='btn btn-sm btn-outline-warning btn-circle btnEditar' ><i class='far fa-edit'></i></button>"
            html_action1 = html_action1 + "<button class='btn btn-sm btn-outline-info btn-circle btnVerTotal ' ><i class='fa fa-list-alt' ></i></button>"
            html_action1 = html_action1 + "<button class='btn btn-sm btn-outline-danger btn-circle btnBorrar ' ><i class='fas fa-users-slash'></i></button>"
            inicio = int(request.GET.get('inicio'))
            fin = int(request.GET.get('limite'))
            list_data=[]
            #obj = Ingresos.objects.filter(estado=True)
            for indice,valor in enumerate(self.get_queryset()[inicio:inicio+fin],inicio):
            #for indice,valor in enumerate(self.get_queryset()):
                objeto = {}
                objeto['num'] = indice +1
                objeto['id'] = str(valor.id) 
                objeto['nombres'] = valor.nombres + ' ' + valor.apellidos
                objeto['fecha_nacimiento'] = str(valor.edad()) + 'años'
                
                objeto['celular'] = valor.celular
                objeto['correo'] =   valor.correo
                objeto['genero'] = str(valor.genero.nombre)
                objeto['action1'] = html_action
                objeto['action2'] = html_action1
            
                list_data.append(objeto)
            
            data = {
                'length': self.get_queryset().count(),
                'objects':list_data
            }

        
            return HttpResponse(json.dumps(data),'aplication/json')
        else:
            template_name = 'paciente/paciente_list.html'
            return render(request, template_name)



class PacienteNew(LoginRequiredMixin, generic.CreateView):
    model = Paciente
    template_name = 'paciente/paciente_form.html'
    context_object_name = 'obj'
    form_class = PacienteForm  
    success_url = reverse_lazy('paciente:paciente_list')
    login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.user_created = self.request.user

        return super().form_valid(form)

class PacienteEdit(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Paciente
    template_name = 'paciente/paciente_form.html'
    context_object_name = 'obj'
    form_class = PacienteForm
    success_url = reverse_lazy('paciente:paciente_list')
    login_url = 'bases:login'
    success_message = "Actializado satisfactoriamente"

    def form_valid(self, form):
        form.instance.user_updated = self.request.user.id

        return super().form_valid(form)

# retorna toda la informacion de paciente 
def paciente_info_view(request):
    
    contexto = {}
    # obj = Paciente.objects.get(pk=id)
    # his = Historia.objects.filter(estado=True).all().order_by('-fecha_consulta')

    # new_obj = []
    # for item in his:
    #     objeto = {}
    #     objeto["id"] = item.id
    #     objeto["fecha_consulta"] = item.fecha_consulta
    #     objeto["fecha_proxima"] = item.fecha_proxima
    #     objeto["descripcion"] = item.descripcion
    #     objeto["proxima_session"] = item.proxima_session
    #     objeto["categoria"] = item.categoria
    #     objeto["medico"] = item.medico

    #     if item.sub_categoria:
    #         # print("tiene")
    #         sub = Sub_categoria.objects.get(pk=item.sub_categoria)
            
    #         objeto["sub_categoria"] = str(sub.nombre)
    #     else:
    #         # print('no')
    #         objeto["sub_categoria"] = 'No registrado'

       

    #     new_obj.append(objeto)
    # if not obj:
    #     return HttpResponse('Subcategoria not ' + str(id))

    if request.method == 'GET':
        # contexto = {'obj': obj, 'his': new_obj}
        id = request.GET.get('id_paciente')
        paciente = Paciente.objects.get(pk=id)
        historia = Historia.objects.filter(paciente_id=id).order_by('fecha_consulta').last()
        numero_historia = Historia.objects.filter(paciente_id=id).all().count()
        
        print(numero_historia)
        
        obj_json = {}
        obj_json["paciente"] = str(paciente)
        obj_json["edad"] = str(paciente.edad())
        if historia:
            fecha_consulta = historia.fecha_consulta
            fecha_consulta = fecha_consulta - timedelta(hours=4)
            fecha_consulta = fecha_consulta.strftime("%d/%m/%Y %H:%M")
            if historia.fecha_proxima: 
                fecha_proxima =  historia.fecha_proxima.strftime("%d/%m/%Y")
            else:
                fecha_proxima = "No hay fecha"
                
            if historia.hora_proxima: 
                hora_proxima =  historia.hora_proxima
            else:
                hora_proxima = "No hay hora"
            obj_json["ultima_session"] = str(fecha_consulta) 
            obj_json["medico"] = str(historia.medico)
            obj_json["tiempo_dif"] =  historia.tiempo_dif()
            obj_json["proxima"] = str(historia.proxima_session)
            obj_json["proxima_session"] = str(fecha_proxima)
            obj_json["hora_proxima"] = str(hora_proxima)

            obj_json["categoria"] = str(historia.categoria)
            obj_json["visitas"] = str(numero_historia)
        else:
            obj_json["ultima_session"] = "No hay registros" 
            obj_json["medico"] = "No hay registros"
            obj_json["tiempo_dif"] = "No hay registros"
            obj_json["proxima"] = "No hay registros"
            obj_json["proxima_session"] = "No hay registros"
            obj_json["categoria"] = "No hay registros"
            obj_json["visitas"] = "No hay registros"
        contexto = {'status': 'OK', 'obj':obj_json}
        return HttpResponse(json.dumps(contexto), content_type=json)


def paciente_disabled(request, id):
    template_name = 'paciente/paciente_disabled.html'
    contexto = {}
    obj = Paciente.objects.get(pk=id)

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




def paciente_view_total(request, id):
    template_name = 'paciente/paciente_view_total.html'
    contexto = {}

    if request.method == 'GET':
        # print('===========================')
        # print(id)
        obj = Paciente.objects.get(pk = id)
        ingresos = Ingresos.objects.filter(paciente_id=id).all()
        total = 0
        if ingresos:
            for i in ingresos: 
                total = total + int( i.monto)

        # print(ingresos)
        contexto = {'obj':ingresos, 'paciente':obj, 'total':total}

    return render(request, template_name, contexto)