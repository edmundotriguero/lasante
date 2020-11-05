from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from django.views import generic
from django.urls import reverse_lazy


from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required



from .models import Especialidad, Medico
from .forms import EspecialidadForm, MedicoForm


#  Clases para Especialidad
class EspecialidadView(LoginRequiredMixin, generic.ListView):
    model = Especialidad
    template_name = 'especialidad/especialidad_list.html'
    context_object_name = 'obj'
    login_url = 'bases:login'

class EspecialidadNew(LoginRequiredMixin, generic.CreateView):
    model = Especialidad
    template_name = 'especialidad/especialidad_form.html'
    context_object_name = 'obj'
    form_class = EspecialidadForm  
    success_url = reverse_lazy('medico:especialidad_list')
    login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.user_created = self.request.user

        return super().form_valid(form)

class EspecialidadEdit(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Especialidad
    template_name = 'especialidad/especialidad_form.html'
    context_object_name = 'obj'
    form_class = EspecialidadForm
    success_url = reverse_lazy('medico:especialidad_list')
    login_url = 'bases:login'
    success_message = "Actializado satisfactoriamente"

    def form_valid(self, form):
        form.instance.user_updated = self.request.user.id

        return super().form_valid(form)


# @login_required(login_url='/login/')
# @permission_required('paciente.delete_genero', login_url='bases:sin_privilegios')
def especialidad_disabled(request, id):
    template_name = 'especialidad/especialidad_disabled.html'
    contexto = {}
    obj = Especialidad.objects.filter(pk=id).first()

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



#  Clases para Especialidad
class MedicoView(LoginRequiredMixin, generic.ListView):
    model = Medico
    template_name = 'medico/medico_list.html'
    context_object_name = 'obj'
    login_url = 'bases:login'

class MedicoNew(LoginRequiredMixin, generic.CreateView):
    model = Medico
    template_name = 'medico/medico_form.html'
    context_object_name = 'obj'
    form_class = MedicoForm  
    success_url = reverse_lazy('medico:medico_list')
    login_url = 'bases:login'

    def form_valid(self, form):
        form.instance.user_created = self.request.user

        return super().form_valid(form)

class MedicoEdit(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Medico
    template_name = 'medico/medico_form.html'
    context_object_name = 'obj'
    form_class = MedicoForm
    success_url = reverse_lazy('medico:medico_list')
    login_url = 'bases:login'
    success_message = "Actializado satisfactoriamente"

    def form_valid(self, form):
        form.instance.user_updated = self.request.user.id

        return super().form_valid(form)


# @login_required(login_url='/login/')
# @permission_required('paciente.delete_genero', login_url='bases:sin_privilegios')
def medico_disabled(request, id):
    template_name = 'medico/medico_disabled.html'
    contexto = {}
    obj = Medico.objects.filter(pk=id).first()

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

