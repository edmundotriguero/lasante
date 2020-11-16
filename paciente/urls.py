from django.urls import path

from .views import GeneroView, GeneroNew, GeneroEdit, genero_disabled, \
    CiudadView, CiudadNew, CiudadEdit, ciudad_disabled, \
    DocumentoView, DocumentoNew, DocumentoEdit, documento_disabled, \
    PacienteView, PacienteNew, paciente_info_view, PacienteEdit ,paciente_disabled

urlpatterns = [
    # cidad para genero
    path('generos/', GeneroView.as_view(), name='genero_list'),
    path('generos/new', GeneroNew.as_view(), name='genero_new'),
    path('generos/edit/<int:pk>',
         GeneroEdit.as_view(), name='genero_edit'),
    path('generos/disabled/<int:id>', genero_disabled, name='genero_disabled'),

    # rutas para ciudad
    path('ciudad/', CiudadView.as_view(), name='ciudad_list'),
    path('ciudad/new', CiudadNew.as_view(), name='ciudad_new'),
    path('ciudad/edit/<int:pk>',
         CiudadEdit.as_view(), name='ciudad_edit'),
    path('ciudad/disabled/<int:id>', ciudad_disabled, name='ciudad_disabled'),

    # rutas para Tipo de documento se coloca solo Documento por temas de simplificacion
    path('documento/', DocumentoView.as_view(), name='documento_list'),
    path('documento/new', DocumentoNew.as_view(), name='documento_new'),
    path('documento/edit/<int:pk>',
         DocumentoEdit.as_view(), name='documento_edit'),
    path('documento/disabled/<int:id>',
         documento_disabled, name='documento_disabled'),


    #rutas para pacientes
    path('paciente/', PacienteView.as_view(), name='paciente_list'),
    path('paciente/new', PacienteNew.as_view(), name='paciente_new'),
    path('paciente/edit/<int:pk>', PacienteEdit.as_view(), name='paciente_edit'),
    path('paciente/disabled/<int:id>', paciente_disabled, name='paciente_disabled'),
    path('paciente/view_info', paciente_info_view), #ajax

]
