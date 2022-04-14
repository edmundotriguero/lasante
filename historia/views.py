from django.shortcuts import render, redirect

from django.views import generic
from django.urls import reverse_lazy

from django.db import transaction


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
from inventario.models import Item, Grupo_um, Unidad_medida, Doc_salida, Consumo_inv
from cajas.models import Ingresos, Tipo_pago


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
    items = Item.objects.filter(estado=True).all()
    pago = Tipo_pago.objects.filter(estado=True).all()
    paciente = Paciente.objects.filter(estado=True,id=id).get()

    if not obj:
        return HttpResponse('Subcategoria not ' + str(id))

    if request.method == 'GET':
        contexto = {'obj': obj, 'cat': cat, 'medico':medico, 'items':items, 'pago':pago, 'paciente':paciente}

    if request.method == 'POST':
        categoria = request.POST.get('categoria')
        subcategoria = request.POST.getlist('subcategoria[]')
        proxima_session = request.POST.get('session')
        descripcion = request.POST.get('descripcion')
        fecha_consulta = request.POST.get('fecha_consulta')
        fecha_proxima_str = request.POST.get('proxima')
        hora = request.POST.get('hora')
        medico = request.POST.get('medico')
        date_format = "%Y-%m-%d"


        iditem = request.POST.getlist('iditem[]')
        idcantidad = request.POST.getlist('idcantidad[]') # total
        idumb = request.POST.getlist('idumb[]')
        multiplicador = request.POST.getlist('multiplicador[]')
        idgrupo = request.POST.getlist('idgrupo[]')


        monto = request.POST.get('monto')
        tipopago = request.POST.get('tipopago')

        print(monto)
        print(tipopago)
        # print(iditem)        
        # print('dato id item')

        if fecha_proxima_str:
            fecha_proxima = datetime.strptime(str(fecha_proxima_str), date_format)
        else: 
            fecha_proxima = None

        # fecha_consulta = datetime.strptime(fecha_consulta, "%d/%m/%Y %H:%M:%S")
        fecha_consulta = datetime.strptime(fecha_consulta, "%Y-%m-%dT%H:%M")
        

        if proxima_session == 'on':
            session = True
        else:
            session = False
        # print("===========")


        #print(subcategoria)

        with transaction.atomic():
            obj = Historia(
                paciente_id=id,
                categoria_id=categoria,
                sub_categoria=subcategoria,
                medico_id=medico,
                proxima_session=session,
                descripcion=descripcion,
                fecha_consulta=fecha_consulta,
                fecha_proxima=fecha_proxima,
                hora_proxima=hora,
                estado=True,
                
                user_created=request.user

            )
            obj.save()
            print(len(idgrupo))
            
            ingreso = Ingresos (
                paciente_id=id,
                detalle=descripcion,
                fecha=fecha_consulta,
                monto=monto,
                estado=True,
                tipo_pago_id=tipopago,
                user_created=request.user,
                hist = obj.id
            )
            ingreso.save()



            if idgrupo:
                with transaction.atomic():
                    doc = Doc_salida (
                        fecha = fecha_consulta,
                        razon = 'tratamiento en visita medica',
                        historia_id= obj.id,
                        user_created= request.user
                    )
                    doc.save()
                    for i in range(int(len(idgrupo))):
                        a = Item.objects.get(pk=iditem[i])
                        u = Unidad_medida.objects.get(pk=idumb[i])
                        
                        inv = Consumo_inv(
                            item=a,
                            doc_salida=doc,
                            cantidad_total=idcantidad[i],
                            unidad_medida_t=u,
                            grupo=idgrupo[i],
                            multiplicador=multiplicador[i],
                            user_created=request.user
                        )
                        inv.save()
                        
                        a1 = a.cantidad
                        # print("cantidades para restar en stock")
                        # print(a1)
                        a2 = idcantidad[i]
                        # print(a2)
                        res = int(a1) - int(a2)
                        a.cantidad = res
                        a.user_updated = request.user.id
                        a.save()

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
        item_list = []
        objeto = {}
        objeto["id"] = item.id
        objeto["fecha_consulta"] = item.fecha_consulta
        objeto["fecha_proxima"] = item.fecha_proxima
        objeto["descripcion"] = item.descripcion
        objeto["proxima_session"] = item.proxima_session
        objeto["hora"] = item.hora_proxima
        objeto["categoria"] = item.categoria
        objeto["medico"] = item.medico

        if item.sub_categoria:
            # print("tiene")
            # sub = Sub_categoria.objects.get(pk=item.sub_categoria)
            
            # objeto["sub_categoria"] = str(sub.nombre)
            if '[' in  item.sub_categoria:

                aux1 = item.sub_categoria[1 : -1]
                lista_aux = aux1.split(',')
                # print("--------------")
                esp = ''
                for item2 in lista_aux:
                    if item2:
                        # print(item2)
                        item2 = item2.strip()
                        sub = Sub_categoria.objects.get(pk=item2[1 : -1])
                        esp = esp + str(sub.nombre) + ", "

                    else: 
                        esp = "No Registrado"   
                objeto["sub_categoria"] = esp[0 : -2]
            else:
                sub = Sub_categoria.objects.get(pk=item.sub_categoria)
            
                objeto["sub_categoria"] = str(sub.nombre)
        else:
            # print('no')
            objeto["sub_categoria"] = 'No registrado'

        doc = Doc_salida.objects.filter(historia_id=item.id).first()
        if doc:
            inv = Consumo_inv.objects.filter(doc_salida=doc.id).all()
            for j in inv:
                aux2 = {}
                aux2["item"] = str(j.item.nombre) + " " + str(j.cantidad_total) + " " + str(j.unidad_medida_t.nombre)
                item_list.append(aux2)
            objeto["item_list"] = item_list
            objeto["item_state"] = True

        else:
            objeto["item_list"] = "Sin items utilizados"
            objeto["item_state"] = False
        
        monto = Ingresos.objects.filter(hist=item.id).first()
        if monto:
            objeto["monto"] = monto.monto
        else:
            objeto["monto"] = "No registrado"
 

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



# se usa por ajax: verifica si existe subcategorias de una categoria: retorna una cadena depende de cada uno.
# para que pueda ser usado en la plantailla 
def item_view_instance(request):
    if request.method == 'GET':
        id_item = request.GET.get('id_item')
        # print(cat)
        item = Item.objects.get(pk=id_item)
        item_u = str(item.cantidad) + " " + str(item.unidad_medida_basica)
        item_um = item.unidad_medida_basica.id
        item_um_n = item.unidad_medida_basica.nombre
        stock = item.cantidad
        aux = ''
        query_json = []
        if item.factor_conversion == True:

            query = Grupo_um.objects.filter(item_id=id_item, estado=True).all()
            aux = 'OK'
            query_json = []
            for itemq in query:
                um = Unidad_medida.objects.get(pk=itemq.unidad_medida)
                objeto = {}
                
                objeto['id'] = itemq.id # id de grupo_um
                objeto['id_um'] = itemq.unidad_medida 
                objeto['unidad_medida'] = um.nombre
                objeto['origen'] = itemq.um_origen

                query_json.append(objeto)
            
        else:
            aux = 'NOT'

        contexto = {'obj': aux, 'sub_categoria':query_json, 'item':item_u, 'item_um':item_um, 'item_um_n':item_um_n, 'stock':stock}
        return HttpResponse(json.dumps(contexto), content_type=json)
    
    return HttpResponse({'obj': 'NONE'})