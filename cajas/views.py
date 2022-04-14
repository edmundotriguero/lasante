
from re import template
from sqlite3 import Date
from django.db.models.base import Model
from django.shortcuts import render, redirect

from django.views import generic
from django.urls import reverse_lazy


from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


from django.http import HttpResponse, StreamingHttpResponse
from django.contrib.auth.decorators import login_required, permission_required
import json
from datetime import datetime

from django.db import connection

from .models import Ingresos, Egresos, Tipo_pago
from .forms import TipopagoForm, IngresoForm, EgresoForm


from paciente.models import Paciente
from medico.models import Medico
from inventario.models import Consumo_inv, Item, Doc_salida,Detalle_Ingreso, Unidad_medida, Doc_ingreso

from historia.models import Sub_categoria

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

# def ingreso_view(request):
    
#     template_name = 'ingreso/ingreso_list.html'
#     contexto = 'obj'
#     obj = Ingresos.objects.all()

#     inicio = request.GET.get('inicio')
#     final = request.GET.get('final')
#     print(inicio)
#     print(type(inicio))
#     if inicio:
#         obj = Ingresos.objects.filter(fecha__range = (inicio, final))

#     if request.method == 'GET':
#         contexto = {'obj': obj}

#     if request.method == 'POST':
        
#         # obj = Ingresos.objects
#         contexto = {'obj': obj}

#     return render(request, template_name, contexto)

class List_ingreso(LoginRequiredMixin, generic.ListView):
    model = Ingresos
    template_name = 'ingreso/ingreso_list.html'
    login_url = 'bases:login'
    


    

    def get_queryset(self):
        

        # f_inicio = self.request.GET.get('')
        # f_final = self.request.GET.get('')

        filtro = self.request.GET.get('filtro')

        query = "SELECT ci.id id, ci.fecha fecha, concat(pa.nombres,' ' ,pa.apellidos) pacie, tp.nombre forma_pago, concat(med.nombres, ' ' , med.apellidos) med, cat.nombre cat,  ci.monto mon" 
        query = query + " from cajas_ingresos ci left JOIN historia_historia his on ci.hist = his.id "
        query = query + "INNER JOIN paciente_paciente pa on pa.id = ci.paciente_id "
        query = query + "INNER JOIN cajas_tipo_pago tp on tp.id = ci.tipo_pago_id "
        query = query + "LEFT JOIN medico_medico med on med.id = his.medico_id "
        query = query + "left join historia_categoria cat on cat.id = his.categoria_id "
        query = query + " where ci.estado = 1 "
        #query = query + " or med.nombres  like '%%"+ filtro + "%%' "
        # query = query + " or med.apellidos  like '%%"+ filtro + "%%' "
        #query = query + " or pa.nombres  like '%%"+ filtro + "%%' "
        query = query + " and pa.apellidos  like '%%"+ filtro + "%%' "
        # query = query + " and ci.fecha BETWEEN str_to_date('" + f_inicio + "','%%Y-%%m-%%d') and  str_to_date('" + f_final + "','%%Y-%%m-%%d')"
#BETWEEN str_to_date('2021-12-01','%Y-%m-%d') and  str_to_date('2021-12-31','%Y-%m-%d')
        query = query + " ORDER by " + self.request.GET.get('order_by') 
        #print(query)
        return self.model.objects.raw( query) #,
                                         #nombre__icontains=self.request.GET.get('filtro')
                                         #).values('id','nombre'
                                         #)

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            #TODO: html_action mejorar para estos botones sean consumidos en front, se coloca aqui como solucion temporal por que no se pudo hacer funciona el columnDefs de dataTable
            html_action = "<button class='btn btn-sm btn-outline-info btn-circle btnImprimir' ><i class='fas fa-print fa-lg'></i></button> "
            html_action = html_action + "<button class='btn btn-sm btn-outline-warning btn-circle btnEditar' ><i class='far fa-edit fa-lg'></i></button>"
            html_action = html_action + "<button class='btn btn-sm btn-outline-danger btn-circle btnBorrar' ><i class='fas fa-ban fa-lg'></i></button>"
            inicio = int(request.GET.get('inicio'))
            fin = int(request.GET.get('limite'))
            list_data=[]
            #obj = Ingresos.objects.filter(estado=True)
            #print(self.get_queryset())
            for indice,valor in enumerate(self.get_queryset()[inicio:inicio+fin],inicio):
            #for indice,valor in enumerate(self.get_queryset()):
                #print(valor.fecha)
                objeto = {}
                objeto['num'] = indice +1
                objeto['id'] = valor.id
                objeto['fecha'] = str(valor.fecha)
                objeto['pacie'] = valor.pacie
                objeto['forma_pago'] = valor.forma_pago
                objeto['med'] =   valor.med
                objeto['cat'] = valor.cat
                objeto['mon'] = valor.mon
                objeto['action'] = html_action
                # #objeto['action'] =  "<button class='btn btn-sm btn-outline-info btn-circle btnImprimir' ><i class='fas fa-print fa-lg'></i></button> 
                # # <button class='btn btn-sm btn-outline-warning btn-circle btnEditar' ><i class='far fa-edit fa-lg'></i></button>
                # #  <button class='btn btn-sm btn-outline-danger btn-circle btnBorrar' ><i class='fas fa-ban fa-lg'></i></button>"

                # #valor['id'] = indice + 1
                list_data.append(objeto)
            
            data = {
                'length': len(list(self.get_queryset())),
                'objects':list_data
            }
            
        
            return HttpResponse(json.dumps(data),'aplication/json')
        else:
            template_name = 'ingreso/ingreso_list.html'
            return render(request, template_name)

# ---------------------

def ingreso_export(request, fecha, fecha1):

    #print(fecha)
    
    #print(fecha1)
    query = "SELECT ci.id id, ci.fecha fecha, concat(pa.nombres,' ' ,pa.apellidos) pacie, tp.nombre forma_pago, concat(med.nombres, ' ' , med.apellidos) med, cat.nombre cat, " 
    query = query + "ci.monto mon, his.id his_id, his.sub_categoria cat_sub" 
    query = query + " from cajas_ingresos ci left JOIN historia_historia his on ci.hist = his.id "
    query = query + "INNER JOIN paciente_paciente pa on pa.id = ci.paciente_id "
    query = query + "INNER JOIN cajas_tipo_pago tp on tp.id = ci.tipo_pago_id "
    query = query + "LEFT JOIN medico_medico med on med.id = his.medico_id "
    query = query + "left join historia_categoria cat on cat.id = his.categoria_id "
    query = query + " where ci.estado = 1 "
    query = query + " and ci.fecha BETWEEN str_to_date('" + fecha + "','%%Y-%%m-%%d') and  str_to_date('" + fecha1 + "','%%Y-%%m-%%d')"
#BETWEEN str_to_date('2021-12-01','%Y-%m-%d') and  str_to_date('2021-12-31','%Y-%m-%d')
    query = query + " ORDER by id" 
    #print(query)
    ingreso = Ingresos.objects.raw(query) 
    
    hoy = Date.today()

    response = StreamingHttpResponse(content_type='text/csv')
    response['Content-Disposition'] = "attachment;filename=report_ingresos_"+str(hoy)+".csv"

    #rows = ("{}|{}\n".format(row.id,row.pacie) for row in ingreso)
    lista = []
    cabecera = "{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format('ID','FECHA','PACIENTE','FORMA DE PAGO','MEDICO','CATEGORIA','SUB CATEGORIA','INSUMOS','MONTO')
    lista.append(cabecera)
    for i in ingreso:
        insumos = ""
        if i.his_id :
            # print(i.his_id)
            # print(type(i.his_id))

            doc = Doc_salida.objects.filter(historia_id = i.his_id).first()
            # print(doc)
            if doc :
                consumo = Consumo_inv.objects.filter(doc_salida = doc.id).all()
                for j in consumo:
                    insumos = insumos + "{} {} {},".format(j.item.nombre, j.cantidad_total, j.unidad_medida_t)
            else:
                insumos = "Sin registro"    
        else:
            insumos = "Sin registro"


        sub_cat = ""

        if i.cat_sub:
            # print("tiene")
            # sub = Sub_categoria.objects.get(pk=item.sub_categoria)
            
            # objeto["sub_categoria"] = str(sub.nombre)
            if '[' in  i.cat_sub:

                aux1 = i.cat_sub[1 : -1]
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
                sub_cat = esp[0 : -2]
            else:
                sub = Sub_categoria.objects.get(pk=item.sub_categoria)
            
                sub_cat = str(sub.nombre)
        else:
            # print('no')
            sub_cat = 'No registrado'


        fila = "{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format(i.id,i.fecha,i.pacie,i.forma_pago,i.med,i.cat,sub_cat,insumos,i.mon)
        lista.append(fila)
    response.streaming_content = lista

    #print(type(rows))
   # print(type(rows))
   # response = HttpResponse('success')
    return response


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

# def egreso_view(request):
    
#     template_name = 'egreso/egreso_list.html'
#     contexto = 'obj'
#     obj = Egresos.objects.all()

#     inicio = request.GET.get('inicio')
#     final = request.GET.get('final')
#     print(inicio)
#     print(type(inicio))
#     if inicio:
#         obj = Egresos.objects.filter(fecha__range = (inicio, final))

#     if request.method == 'GET':
#         contexto = {'obj': obj}

#     # if request.method == 'POST':
        
#     #     # obj = Ingresos.objects
#     #     contexto = {'obj': obj}

#     return render(request, template_name, contexto)




class List_egreso(LoginRequiredMixin, generic.ListView):
    model = Egresos
    template_name = 'egreso/egreso_list.html'
    login_url = 'bases:login'


    def get_queryset(self):


        filtro = self.request.GET.get('filtro')


        

        #return self.model.objects.raw(query)
        return self.model.objects.filter(estado=1)

     
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            html_action = "<button class='btn btn-sm btn-outline-info btn-circle btnImprimir' ><i class='fas fa-print fa-lg'></i></button> "
            html_action = html_action + "<button class='btn btn-sm btn-outline-warning btn-circle btnEditar' ><i class='far fa-edit fa-lg'></i></button>"
            html_action = html_action + "<button class='btn btn-sm btn-outline-danger btn-circle btnBorrar' ><i class='fas fa-ban fa-lg'></i></button>"
            inicio = int(request.GET.get('inicio'))
            fin = int(request.GET.get('limite'))

            list_data=[]

            for indice, valor in enumerate(self.get_queryset()[inicio:inicio+fin],inicio):
                
                objeto = {}
                objeto['num'] = indice+1
                objeto['id'] = valor.id
                objeto['fecha'] = str(valor.fecha)
                objeto['num_factura'] = valor.num_factura
                objeto['tipo_pago'] = valor.tipo_pago.nombre
                objeto['detalle'] = valor.detalle
                objeto['monto'] = valor.monto
                objeto['action'] = html_action



                list_data.append(objeto)

            data = {
                'length': len(list(self.get_queryset())),
                'objects':list_data
            }    

            return HttpResponse(json.dumps(data),'aplication/json')
        else:
            template_name = 'egreso/egreso_list.html'
            return render(request, template_name)



def egreso_export(request, fecha, fecha1):

    #print(fecha)
    
    #print(fecha1)
#     query = "SELECT ci.id id, ci.fecha fecha, concat(pa.nombres,' ' ,pa.apellidos) pacie, tp.nombre forma_pago, concat(med.nombres, ' ' , med.apellidos) med, cat.nombre cat, " 
#     query = query + "ci.monto mon, his.id his_id, his.sub_categoria cat_sub" 
#     query = query + " from cajas_ingresos ci left JOIN historia_historia his on ci.hist = his.id "
#     query = query + "INNER JOIN paciente_paciente pa on pa.id = ci.paciente_id "
#     query = query + "INNER JOIN cajas_tipo_pago tp on tp.id = ci.tipo_pago_id "
#     query = query + "LEFT JOIN medico_medico med on med.id = his.medico_id "
#     query = query + "left join historia_categoria cat on cat.id = his.categoria_id "
#     query = query + " where ci.estado = 1 "
#     query = query + " and ci.fecha BETWEEN str_to_date('" + fecha + "','%%Y-%%m-%%d') and  str_to_date('" + fecha1 + "','%%Y-%%m-%%d')"
# #BETWEEN str_to_date('2021-12-01','%Y-%m-%d') and  str_to_date('2021-12-31','%Y-%m-%d')
#     query = query + " ORDER by id" 
    #print(query)
    egreso = Egresos.objects.filter(estado=1)
    

    response = StreamingHttpResponse(content_type='text/csv')
    response['Content-Disposition'] = "attachment;filename=report_egresos.csv"

    #rows = ("{}|{}\n".format(row.id,row.pacie) for row in ingreso)
    lista = []
    cabecera = "{}|{}|{}|{}|{}|{}\n".format('ID','FECHA','NUM DOC','FORMA DE PAGO','DETALLE','MONTO')
    lista.append(cabecera)
    for i in egreso:
        

        fila = "{}|{}|{}|{}|{}|{}\n".format(i.id,str(i.fecha),i.num_factura,i.tipo_pago.nombre,i.detalle,i.monto)
        lista.append(fila)
    response.streaming_content = lista

    #print(type(rows))
   # print(type(rows))
   # response = HttpResponse('success')
    return response



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


# class EgresoNew(LoginRequiredMixin, generic.CreateView):
#     model = Egresos
#     template_name = 'egreso/egreso_form.html'
#     context_object_name = 'obj'
#     form_class = EgresoForm  
#     success_url = reverse_lazy('cajas:egreso_list')
#     login_url = 'bases:login'

#     # def get_context_data(self, **kwargs):


#     def form_valid(self, form):
#         # fecha = self.request.POST.get('fecha')
#         # fecha = datetime.strptime(fecha, "%d/%m/%Y")
#         # form.instance.fecha = fecha
#         form.instance.user_created = self.request.user

#         return super().form_valid(form)


def egreso_new(request):
    template_name = 'egreso/egreso_form.html'
    contexto = {}
    form = EgresoForm()
    
    items = Item.objects.filter(estado=True).all()


    

    if request.method == 'GET':
        contexto = { 'form':form, 'items':items}

    if request.method == 'POST':
        form = EgresoForm(request.POST)
        if form.is_valid():
            egre = form.save(commit=False)
            egre.user_created = request.user
            egre.save()
            # print(egre.id)  
            # print("id de formulario de salida ") 


        iditem = request.POST.getlist('iditem[]')
        idcantidad = request.POST.getlist('idcantidad[]') # total
        idumb = request.POST.getlist('idumb[]')
        multiplicador = request.POST.getlist('multiplicador[]')
        idgrupo = request.POST.getlist('idgrupo[]')


       
        if idgrupo:
            doc = Doc_ingreso (
                fecha = egre.fecha,
                razon = 'Ingreso por compra de insumos',
                egreso_id= egre.id,
                user_created= request.user
            )
            doc.save()
            for i in range(int(len(idgrupo))):
                a = Item.objects.get(pk=iditem[i])
                u = Unidad_medida.objects.get(pk=idumb[i])
                
                inv = Detalle_Ingreso(
                    item=a,
                    doc_ingreso=doc,
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
                res = int(a1) + int(a2)
                a.cantidad = res
                a.user_updated = request.user.id
                a.save()

        # return HttpResponse('Reegistro Inactivo !!!')
        return redirect("cajas:egreso_list")

    return render(request, template_name, contexto)

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
    
    i = Doc_ingreso.objects.filter(egreso_id=obj.id).first()
    if i:
        obj_list = []
        ingreso = Detalle_Ingreso.objects.filter(doc_ingreso=i.id)
        for j in ingreso:
            objeto = {}
            objeto["item"] = str(j.item.nombre) + " " + str(j.cantidad_total) + " " + str(j.unidad_medida_t.nombre)
            obj_list.append(objeto)
        obj.detalle = obj_list

    today = obj.fecha
    year = obj.fecha.year


    if not obj:
        return HttpResponse('Registro no encontrado ' + str(id))

    if request.method == 'GET':
        contexto = {'obj': obj, 'today':today, 'year':year}

   

    return render(request, template_name, contexto)