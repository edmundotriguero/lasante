from django.shortcuts import render

from django.views import generic
from django.urls import reverse_lazy


from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required

import json
from datetime import datetime, timedelta


from .models import Unidad_medida, Item, Marca, Grupo_um
from .forms import Unidad_medidaForm, MarcaForm, ItemForm




#  Clases para Unidad de medida
class UnidadMedidaView(LoginRequiredMixin, generic.ListView):
    model = Unidad_medida
    template_name = 'unidad_medida/unidadmedida_list.html'
    context_object_name = 'obj'
    login_url = 'bases:login'

class UnidadMedidaNew(LoginRequiredMixin, generic.CreateView):
    model = Unidad_medida
    template_name = 'unidad_medida/unidadmedida_form.html'
    context_object_name = 'obj'
    form_class = Unidad_medidaForm  
    success_url = reverse_lazy('inventario:unidadmedida_list')
    login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.user_created = self.request.user

        return super().form_valid(form)

class UnidadMedidaEdit(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Unidad_medida
    template_name = 'unidad_medida/unidadmedida_form.html'
    context_object_name = 'obj'
    form_class = Unidad_medidaForm
    success_url = reverse_lazy('inventario:unidadmedida_list')
    login_url = 'bases:login'
    success_message = "Actializado satisfactoriamente"

    def form_valid(self, form):
        form.instance.user_updated = self.request.user.id

        return super().form_valid(form)


# @login_required(login_url='/login/')
# @permission_required('paciente.delete_genero', login_url='bases:sin_privilegios')
def unidadmedida_disabled(request, id):
    template_name = 'unidad_medida/unidadmedida_disabled.html'
    contexto = {}
    obj = Unidad_medida.objects.filter(pk=id).first()

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



#  Clases para Marca de items
class MarcaView(LoginRequiredMixin, generic.ListView):
    model = Marca
    template_name = 'marca/marca_list.html'
    context_object_name = 'obj'
    login_url = 'bases:login'

class MarcaNew(LoginRequiredMixin, generic.CreateView):
    model = Marca
    template_name = 'marca/marca_form.html'
    context_object_name = 'obj'
    form_class = MarcaForm  
    success_url = reverse_lazy('inventario:marca_list')
    login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.user_created = self.request.user

        return super().form_valid(form)

class MarcaEdit(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Marca
    template_name = 'marca/marca_form.html'
    context_object_name = 'obj'
    form_class = MarcaForm
    success_url = reverse_lazy('inventario:marca_list')
    login_url = 'bases:login'
    success_message = "Actializado satisfactoriamente"

    def form_valid(self, form):
        form.instance.user_updated = self.request.user.id

        return super().form_valid(form)


# @login_required(login_url='/login/')
# @permission_required('paciente.delete_genero', login_url='bases:sin_privilegios')
def marca_disabled(request, id):
    template_name = 'marca/marca_disabled.html'
    contexto = {}
    obj = Marca.objects.filter(pk=id).first()

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


# Clases para iTEMS

class ItemView(LoginRequiredMixin, generic.ListView):
    model = Item
    template_name = 'item/item_list.html'
    context_object_name = 'obj'
    login_url = 'bases:login'


class ItemNew(LoginRequiredMixin, generic.CreateView):
    model = Item
    template_name = 'item/item_form.html'
    context_object_name = 'obj'
    form_class = ItemForm
    success_url = reverse_lazy('inventario:item_list')
    login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.user_created = self.request.user

        return super().form_valid(form)


class ItemEdit(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Item
    template_name = 'item/item_form.html'
    context_object_name = 'obj'
    form_class = ItemForm
    success_url = reverse_lazy('inventario:item_list')
    login_url = 'bases:login'
    success_message = "Actializado satisfactoriamente"

    def form_valid(self, form):
        form.instance.user_updated = self.request.user.id

        return super().form_valid(form)

# @login_required(login_url='/login/')
# @permission_required('paciente.delete_genero', login_url='bases:sin_privilegios')


def item_disabled(request, id):
    template_name = 'item/item_disabled.html'
    contexto = {}
    obj = Item.objects.filter(pk=id).first()

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



# Clases para Unidad de venta

# @login_required(login_url='/login/')
# @permission_required('paciente.delete_genero', login_url='bases:sin_privilegios')
def grupo_um_list(request, id):
    template_name = 'grupo_um/grupo_um_form.html'
    contexto = {}
    item = Item.objects.get(pk=id)
    obj = Grupo_um.objects.filter(item=id).all()
    obj_json = []
    for i in obj:
        objeto = {}
        objeto['id'] = i.id
        objeto['um_origen'] = str(i.um_origen) + ' ' + str(i.item.unidad_medida_basica)
        um = Unidad_medida.objects.get(pk=i.unidad_medida)
        objeto['um_equivalencia'] = str(i.um_equivalencia) + ' ' + str(um.nombre )
        objeto['estado'] = i.estado
        obj_json.append(objeto)

    if not item:
        return HttpResponse('Registro no existe' + str(id))

    if request.method == 'GET':
        contexto = {'obj': obj_json, 'item': item}

    return render(request, template_name, contexto)


def grupo_um_new(request, id):
    "utilizado por AJAX"

    if request.method == 'POST':

        um_origen = request.POST.get('um_origen')
        um_destino = request.POST.get('um_destino')
        unidad_medida = request.POST.get('unidad_medida')

        if request.POST.get('estado') == 'on':
            estado = True
        else:
            estado = False
        # es para editar el registro
        if request.POST.get('grupo_um'):
            id_grupo_um = request.POST.get('grupo_um')
            obj = Grupo_um.objects.filter(id=id_grupo_um).first()
            obj.um_origen = um_origen
            obj.um_equivalencia = um_destino
            obj.unidad_medida = unidad_medida
            obj.estado = estado
            # sub_product.product_id = id
            obj.user_updated = request.user.id
            obj.save()
            print('Registro editado')
        else:
            obj = Grupo_um
            obj = Grupo_um(
                um_origen=um_origen,
                um_equivalencia=um_destino,
                unidad_medida=unidad_medida,
                estado=estado,
                item_id=id,
                user_created=request.user

            )
            obj.save()

        return HttpResponse('ok')


def grupo_um_view_id(request, id):
    contexto = {}
    if request.method == 'GET':
        grupo_um = Grupo_um.objects.filter(pk=id).first()
        print(grupo_um)
        obj_json = []
        # for item in sub_product:
        objeto_order = {}
        objeto_order["id"] = grupo_um.id
        objeto_order["um_origen"] = grupo_um.um_origen
        objeto_order["um_destino"] = grupo_um.um_equivalencia
        objeto_order["unidad_medida"] = grupo_um.unidad_medida

        # objeto_order["img"] = sub_product.img
        objeto_order["estado"] = grupo_um.estado

        obj_json.append(objeto_order)
        contexto = {'obj': 'OK', 'sub_categoria': obj_json}
        return HttpResponse(json.dumps(contexto), content_type=json)


def grupo_um_disabled(request, id):
    template_name = 'grupo_um/grupo_um_disabled.html'
    contexto = {}
    obj = Grupo_um.objects.get(pk=id)

    if not obj:
        return HttpResponse('UM not ' + str(id))

    if request.method == 'GET':
        contexto = {'obj': obj}

    if request.method == 'POST':
        obj.estado = False
        obj.user_updated = request.user.id
        obj.save()
        contexto = {'obj': 'OK'}
        return HttpResponse('Reegistro Inactivo !!!!')

    return render(request, template_name, contexto)



# se usa por ajax: verifica si existe unidades de medida : retorna una cadena indicando si existe o no instancias.
# para que pueda ser usado en la plantailla 
def um_view_instance(request):
    if request.method == 'GET':
        
        
        um = Unidad_medida.objects.filter(estado=1).all()
        aux = ''
        query_json = []
        
        aux = 'OK'
        query_json = []
        for item in um:
            objeto = {}
            objeto['id'] = item.id
            objeto['nombre'] = item.nombre

            query_json.append(objeto)
            
        

        contexto = {'obj': aux, 'um':query_json}
        return HttpResponse(json.dumps(contexto), content_type=json)
    
    return HttpResponse({'obj': 'NONE'})