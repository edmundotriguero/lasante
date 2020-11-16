from django import forms

from .models import Especialidad, Medico, Turno

# formulario para Genero
class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre','estado']
        labels = {'nombre':'Nombre','estado':'Estado'}
        widget = {'nombre': forms.TextInput, 'estado':forms.CheckboxInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control', 'autocomplete':'off'})
        # self.fields['estado'].widget.attrs.update({'class':'form-control custom-file-input'})

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['nombre','detalles','estado']
        labels = {'nombre':'Nombre','detalles':'Detalles','estado':'Estado'}
        widget = {'nombre': forms.TextInput, 'estado':forms.CheckboxInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control', 'autocomplete':'off'})
        # self.fields['estado'].widget.attrs.update({'class':'form-control custom-file-input'})

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['nombres','apellidos','tipo_documento','documento_identificacion','fecha_nacimiento','especialidad','turno','genero','ciudad','celular','correo','estado']
        labels = {'nombres':'Nombres','apellidos':'Apellido','tipo_documento':'Tipo documento','fecha_nacimiento':'Fecha de Nacimiento', 'especialidad':'Especialidad', 'genero':'Genero', 'ciudad':'Ciudad', 'celular':'Celular', 'correo':'Correo',  'estado':'Estado'}
        widget = {'nombres': forms.TextInput, 'estado':forms.CheckboxInput, 'correo':forms.EmailInput, 'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'} ) }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control form-control-sm', 'autocomplete':'off'})
        # self.fields['fecha_nacimiento'].widget.attrs.update({'autocomplete':'on', 'type':'date'})
