from django.urls import path
from .views import CategoriaView, CategoriaNew, CategoriaEdit, categoria_disabled, \
                    subcategoria_list, sub_categoria_new, subcategoria_view_id, subcategoria_disabled


urlpatterns = [
    # cidad para Categoria
    path('categoria/', CategoriaView.as_view(), name='categoria_list'),
    path('categoria/new', CategoriaNew.as_view(), name='categoria_new'),
    path('categoria/edit/<int:pk>',
         CategoriaEdit.as_view(), name='categoria_edit'),
    path('categoria/disabled/<int:id>', categoria_disabled, name='categoria_disabled'),

    # urls para sub categorias
    path('subcategoria/list/<int:id>', subcategoria_list, name='subcategoria_list'),
    path('subcategoria_id/view/<int:id>', subcategoria_view_id, name='subcategoria_id'),  #ajax
    path('sub_categoria/new/<int:id>', sub_categoria_new, name='subcategoria_new'),       #ajax
    

]