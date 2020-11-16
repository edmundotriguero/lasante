from django.shortcuts import render, redirect

from django.views import generic
from django.urls import reverse_lazy


from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
import json
from datetime import datetime

from .models import Categoria, Sub_categoria, Historia
from .forms import CategoriaForm


from paciente.models import Paciente
from medico.models import Medico


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
        contexto = {'obj': obj, 'cat': cat}

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
        return HttpResponse('Reegistro Inactivo !!!')

    return render(request, template_name, contexto)


# vistas para historia

def historia_new(request, id):
    template_name = 'historia/historia_new.html'
    contexto = {}
    obj = Paciente.objects.filter(pk=id).first()
    cat = Categoria.objects.filter(estado=True).all()
    medico = Medico.objects.filter(estado=True).all()


    if not obj:
        return HttpResponse('Subcategoria not ' + str(id))

    if request.method == 'GET':
        contexto = {'obj': obj, 'cat': cat, 'medico':medico}

    if request.method == 'POST':
        categoria = request.POST.get('categoria')
        subcategoria = request.POST.get('subcategoria')
        proxima_session = request.POST.get('session')
        descripcion = request.POST.get('descripcion')
        fecha_consulta = request.POST.get('fecha_consulta')
        fecha_proxima_str = request.POST.get('proxima')
        medico = request.POST.get('medico')
        date_format = "%Y-%m-%dT%H:%M"
        if fecha_proxima_str:
            fecha_proxima = datetime.strptime(str(fecha_proxima_str), date_format)
        else: 
            fecha_proxima = None
        fecha_consulta = datetime.strptime(fecha_consulta, "%d/%m/%Y %H:%M:%S")
        
        if proxima_session == 'on':
            session = True
        else:
            session = False

        obj = Historia(
            paciente_id=id,
            categoria_id=categoria,
            sub_categoria=subcategoria,
            medico_id=medico,
            proxima_session=session,
            descripcion=descripcion,
            fecha_consulta=fecha_consulta,
            fecha_proxima=fecha_proxima,
            estado=True,
            
            user_created=request.user

        )
        obj.save()
        # return HttpResponse('Reegistro Inactivo !!!')
        return redirect("paciente:paciente_list")

    return render(request, template_name, contexto)


def historia_list(request, id):
    template_name = 'historia/historia_list.html'
    contexto = {}
    obj = Paciente.objects.get(pk=id)
    his = Historia.objects.filter(estado=True, paciente_id=id).all().order_by('-fecha_consulta')

    new_obj = []
    for item in his:
        objeto = {}
        objeto["id"] = item.id
        objeto["fecha_consulta"] = item.fecha_consulta
        objeto["fecha_proxima"] = item.fecha_proxima
        objeto["descripcion"] = item.descripcion
        objeto["proxima_session"] = item.proxima_session
        objeto["categoria"] = item.categoria
        objeto["medico"] = item.medico

        if item.sub_categoria:
            # print("tiene")
            sub = Sub_categoria.objects.get(pk=item.sub_categoria)
            
            objeto["sub_categoria"] = str(sub.nombre)
        else:
            # print('no')
            objeto["sub_categoria"] = 'No registrado'

       

        new_obj.append(objeto)
    if not obj:
        return HttpResponse('Subcategoria not ' + str(id))

    if request.method == 'GET':
        contexto = {'obj': obj, 'his': new_obj}

   

    return render(request, template_name, contexto)


# se usa por ajax: verifica si existe subcategorias de una categoria: retorna una cadena depende de cada uno.
# para que pueda ser usado en la plantailla 
def categoria_view_instance(request):
    if request.method == 'GET':
        cat = request.GET.get('id_categoria')
        print(cat)
        categoria = Categoria.objects.get(pk=cat)
        aux = ''
        query_json = []
        if categoria.subcategoria_estado == True:

            query = Sub_categoria.objects.filter(categoria_id=cat, estado=True).all()
            aux = 'OK'
            query_json = []
            for item in query:
                objeto = {}
                objeto['id'] = item.id
                objeto['nombre'] = item.nombre

                query_json.append(objeto)
            
        else:
            aux = 'NOT'

        contexto = {'obj': aux, 'sub_categoria':query_json}
        return HttpResponse(json.dumps(contexto), content_type=json)
    
    return HttpResponse({'obj': 'NONE'})