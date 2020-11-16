from django import forms

from .models import Genero, Ciudad, Tipo_documento, Paciente

# formulario para Genero
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


# formulario para Ciudad
class CiudadForm(forms.ModelForm):
    class Meta:
        model = Ciudad
        fields = ['nombre','estado']
        labels = {'nombre':'Nombre','estado':'Estado'}
        widget = {'nombre': forms.TextInput, 'estado':forms.CheckboxInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control', 'autocomplete':'off'})
        # self.fields['estado'].widget.attrs.update({'class':'form-control custom-file-input'})


# formulario para Ciudad
class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Tipo_documento
        fields = ['nombre','estado']
        labels = {'nombre':'Nombre','estado':'Estado'}
        widget = {'nombre': forms.TextInput, 'estado':forms.CheckboxInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control', 'autocomplete':'off'})

# formulario para pacientes
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombres','apellidos','tipo_documento','documento_identificacion','fecha_nacimiento','genero','ciudad','celular','correo','estado']
        # labels = {'nombre':'Nombre','estado':'Estado'}
        widget = {'fecha_nacimiento': forms.DateInput() }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control form-control-sm', 'autocomplete':'off'})