from django.urls import path

from .views import GeneroView, GeneroNew, GeneroEdit, genero_disabled

urlpatterns = [
    path('generos/', GeneroView.as_view(), name='genero_list'),
    path('generos/new', GeneroNew.as_view(), name='genero_new'),
    path('generos/edit/<int:pk>',
         GeneroEdit.as_view(), name='genero_edit'),
    path('generos/disabled/<int:id>', genero_disabled, name='genero_disabled'),
]
