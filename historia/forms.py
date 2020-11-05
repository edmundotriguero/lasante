from django import forms

from .models import Categoria, Sub_categoria, Historia

# formulario para Categoria
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre','descripcion','estado','subcategoria_estado']
        labels = {'nombre':'Nombre','estado':'Estado'}
        # widget = {'nombre': forms.TextInput, 'estado':forms.CheckboxInput}

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in iter(self.fields):
    #         self.fields[field].widget.attrs.update({'class':'form-control', 'autocomplete':'off'})
        # self.fields['estado'].widget.attrs.update({'class':'form-control custom-file-input'})