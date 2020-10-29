from django.shortcuts import render

from django.views import generic
from django.urls import reverse_lazy


from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import Genero

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required

from .forms import GeneroForm


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
