from django.urls import path

from .views import List_ingreso, ingreso_new, IngresoEdit, ingreso_disabled, ingreso_print, ingreso_export,\
    TipopagoView, TipopagoNew, TipopagoEdit, tipopago_disabled, \
    List_egreso, egreso_new, EgresoEdit, egreso_disabled, egreso_print, egreso_export
urlpatterns = [
    # cidad para igreso
    path('ingreso/', List_ingreso.as_view(), name='ingreso_list'),

    # path('ingreso/', ingreso_view, name='ingreso_list'),
    # path('ingreso/GET', ingreso_view, name='ingreso_list'),
    path('ingreso/new/<int:id>', ingreso_new, name='ingreso_new'),
    path('ingreso/edit/<int:pk>',
         IngresoEdit.as_view(), name='ingreso_edit'),
    path('ingreso/disabled/<int:id>', ingreso_disabled, name='ingreso_disabled'),
    path('ingreso/print/<int:id>', ingreso_print, name='ingreso_print'),
    path('ingreso/export/<str:fecha>/<str:fecha1>',
         ingreso_export, name='ingreso_export'),


    # url para egreso

    path('egreso/', List_egreso.as_view(), name='egreso_list'),
    # path('egreso/', egreso_view, name='egreso_list'),
    # path('egreso/GET', egreso_view, name='egreso_list'),


    path('egreso/new', egreso_new, name='egreso_new'),
    path('egreso/edit/<int:pk>',
         EgresoEdit.as_view(), name='egreso_edit'),
    path('egreso/disabled/<int:id>', egreso_disabled, name='egreso_disabled'),
    path('egreso/print/<int:id>', egreso_print, name='egreso_print'),


    path('egreso/export/<str:fecha>/<str:fecha1>',
         egreso_export, name='egreso_export'),
    # cidad para genero
    path('tipopago/', TipopagoView.as_view(), name='tipopago_list'),
    path('tipopago/new', TipopagoNew.as_view(), name='tipopago_new'),
    path('tipopago/edit/<int:pk>',
         TipopagoEdit.as_view(), name='tipopago_edit'),
    path('tipopago/disabled/<int:id>',
         tipopago_disabled, name='tipopago_disabled'),

]
