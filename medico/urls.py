from django.urls import path
from .views import EspecialidadView, EspecialidadNew, EspecialidadEdit, especialidad_disabled, \
    MedicoView, MedicoNew, MedicoEdit, medico_disabled


urlpatterns = [
    # cidad para especialidades
    path('especialidad/', EspecialidadView.as_view(), name='especialidad_list'),
    path('especialidad/new', EspecialidadNew.as_view(), name='especialidad_new'),
    path('especialidad/edit/<int:pk>',
         EspecialidadEdit.as_view(), name='especialidad_edit'),
    path('especialidad/disabled/<int:id>',
         especialidad_disabled, name='especialidad_disabled'),

    # cidad para medicos
    path('medico/', MedicoView.as_view(), name='medico_list'),
    path('medico/new', MedicoNew.as_view(), name='medico_new'),
    path('medico/edit/<int:pk>',
         MedicoEdit.as_view(), name='medico_edit'),
    path('medico/disabled/<int:id>', medico_disabled, name='medico_disabled'),


]
