from django.shortcuts import render

from django.views import generic
from django.urls import reverse_lazy


from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
import json

from .models import Categoria, Sub_categoria, Historia
from .forms import CategoriaForm 


# Clases para Categoria

class CategoriaView(LoginRequiredMixin, generic.ListView):
    model = Categoria
    template_name = 'categoria/categoria_list.html'
    context_object_name = 'obj'
    login_url = 'bases:login'


class CategoriaNew(LoginRequiredMixin, generic.CreateView):
    model = Categoria
    template_name = 'categoria/categoria_form.html'
    context_object_name = 'obj'
    form_class = CategoriaForm  
    success_url = reverse_lazy('historia:categoria_list')
    login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.user_created = self.request.user

        return super().form_valid(form)

class CategoriaEdit(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Categoria
    template_name = 'categoria/categoria_form.html'
    context_object_name = 'obj'
    form_class = CategoriaForm
    success_url = reverse_lazy('historia:categoria_list')
    login_url = 'bases:login'
    success_message = "Actializado satisfactoriamente"

    def form_valid(self, form):
        form.instance.user_updated = self.request.user.id

        return super().form_valid(form)

# @login_required(login_url='/login/')
# @permission_required('paciente.delete_genero', login_url='bases:sin_privilegios')
def categoria_disabled(request, id):
    template_name = 'categoria/categoria_disabled.html'
    contexto = {}
    obj = Categoria.objects.filter(pk=id).first()

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



# Clases para sub Categoria

# @login_required(login_url='/login/')
# @permission_required('paciente.delete_genero', login_url='bases:sin_privilegios')
def subcategoria_list(request, id):
    template_name = 'subcategoria/subcategoria_form.html'
    contexto = {}
    cat = Categoria.objects.get(pk=id)
    obj = Sub_categoria.objects.filter(categoria=id).all()

    if not cat:
        return HttpResponse('Registro no existe' + str(id))

    if request.method == 'GET':
        contexto = {'obj': obj, 'cat':cat}
     

    return render(request, template_name, contexto)



def sub_categoria_new(request, id):
    "utilizado por AJAX"

    if request.method == 'POST':

        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        
        if request.POST.get('estado') == 'on':
            estado = True
        else:
            estado = False
        # es para editar el registro
        if request.POST.get('sub_categoria'):
            id_sub_categoria = request.POST.get('sub_categoria')
            obj = Sub_categoria.objects.filter(id=id_sub_categoria).first()
            obj.nombre = nombre
            obj.descripcion = descripcion
            obj.estado = estado
            # sub_product.product_id = id
            obj.user_updated = request.user.id
            obj.save()
            print('Editar registro')
        else:
            obj = Sub_categoria
            obj = Sub_categoria(
                nombre=nombre,
                descripcion=descripcion,
                estado=estado,
                categoria_id=id,
                user_created=request.user

            )
            obj.save()

        return HttpResponse('ok')   

def subcategoria_view_id(request, id):
    contexto = {}
    if request.method == 'GET':
        sub_categoria = Sub_categoria.objects.filter(pk=id).first()
        
        obj_json = []
        # for item in sub_product:
        objeto_order = {}
        objeto_order["id"] = sub_categoria.id
        objeto_order["nombre"] = sub_categoria.nombre
        objeto_order["descripcion"] = sub_categoria.descripcion
       

        # objeto_order["img"] = sub_product.img
        objeto_order["estado"] = sub_categoria.estado

        obj_json.append(objeto_order)
        contexto = {'obj': 'OK', 'sub_categoria': obj_json}
        return HttpResponse(json.dumps(contexto), content_type=json)



def subcategoria_disabled(request, id):
    template_name = 'subcategoria/subcategoria_disabled.html'
    contexto = {}
    obj = Sub_categoria.objects.filter(pk=id).first()

    if not obj:
        return HttpResponse('Subcategoria not ' + str(id))

    if request.method == 'GET':
        contexto = {'obj': obj}

    if request.method == 'POST':
        obj.estado = False
        obj.user_updated = request.user.id
        obj.save()
        contexto = {'obj': 'OK'}
        return HttpResponse('Reegistro Inactivo')

    return render(request, template_name, contexto)