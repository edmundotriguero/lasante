from django import forms

from .models import Genero

# formulario para categorias
class GeneroForm(forms.ModelForm):
    class Meta:
        model = Genero
        fields = ['nombre','estado']
        labels = {'nombre':'Nombre','estado':'Estado'}
        widget = {'nombre': forms.TextInput, 'estado':forms.CheckboxInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control', 'autocomplete':'off'})
        # self.fields['estado'].widget.attrs.update({'class':'form-control custom-file-input'})
