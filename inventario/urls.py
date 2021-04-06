from django.urls import path
from .views import UnidadMedidaView, UnidadMedidaNew, UnidadMedidaEdit, unidadmedida_disabled,\
    MarcaView, MarcaNew, MarcaEdit, marca_disabled, \
    ItemView, ItemNew, ItemEdit, item_disabled, \
    grupo_um_list, um_view_instance, grupo_um_new, grupo_um_view_id, grupo_um_disabled


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

]
