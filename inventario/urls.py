from django.urls import path
from .views import UnidadMedidaView, UnidadMedidaNew, UnidadMedidaEdit, unidadmedida_disabled,\
    MarcaView, MarcaNew, MarcaEdit, marca_disabled, \
    ItemView, ItemNew, ItemEdit, item_disabled, \
    grupo_um_list, um_view_instance, grupo_um_new, grupo_um_view_id, grupo_um_disabled, \
    ingreso_stock_view, ingreso_stock_new, ingreso_stock_print, \
    salida_stock_view, salida_stock_new, salida_stock_print


urlpatterns = [

    # unidad de medida
    path('unidadmedida/', UnidadMedidaView.as_view(), name='unidadmedida_list'),
    path('unidadmedida/new', UnidadMedidaNew.as_view(), name='unidadmedida_new'),
    path('unidadmedida/edit/<int:pk>',
         UnidadMedidaEdit.as_view(), name='unidadmedida_edit'),
    path('unidadmedida/disabled/<int:id>',
         unidadmedida_disabled, name='unidadmedida_disabled'),
    #  marca
    path('marca/', MarcaView.as_view(), name='marca_list'),
    path('marca/new', MarcaNew.as_view(), name='marca_new'),
    path('marca/edit/<int:pk>',
         MarcaEdit.as_view(), name='marca_edit'),
    path('marca/disabled/<int:id>', marca_disabled, name='marca_disabled'),

    # items
    path('item/', ItemView.as_view(), name='item_list'),
    path('item/new', ItemNew.as_view(), name='item_new'),
    path('item/edit/<int:pk>',
         ItemEdit.as_view(), name='item_edit'),
    path('item/disabled/<int:id>', item_disabled, name='item_disabled'),


    # urls para grupos de unidades de medida   Grupo_um
    path('grupo_um/list/<int:id>', grupo_um_list, name='grupo_um_list'),
    path('grupo_um_id/view/<int:id>', grupo_um_view_id,
         name='grupo_um_view_id'),  # ajax
    path('grupo_um/new/<int:id>', grupo_um_new, name='grupo_um_new'),  # ajax
    path('grupo_um/disabled/<int:id>',
         grupo_um_disabled, name='grupo_um_disabled'),

    # ajax
    path('um/view_instance', um_view_instance),


     # vistas para ingreso de stock
    path('ingreso_stock/', ingreso_stock_view, name='ingreso_stock_list'),
    path('ingreso_stock/GET', ingreso_stock_view, name='ingreso_stock_list'),
    path('ingreso_stock/new', ingreso_stock_new, name='ingreso_stock_new'),
    path('ingreso_stock/print/<int:id>', ingreso_stock_print, name='ingreso_stock_print'),

    # vistas para salida de stock
    path('salida_stock/', salida_stock_view, name='salida_stock_list'),
    path('salida_stock/GET', salida_stock_view, name='salida_stock_list'),
    path('salida_stock/new', salida_stock_new, name='salida_stock_new'),
    path('salida_stock/print/<int:id>', salida_stock_print, name='salida_stock_print'),




]
