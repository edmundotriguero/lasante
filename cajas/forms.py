from django import forms


from .models import Tipo_pago, Ingresos, Egresos

# formulario para tipo de pago
class TipopagoForm(forms.ModelForm):
    class Meta:
        model = Tipo_pago
        fields = ['nombre','estado']
        labels = {'nombre':'Nombre','estado':'Estado'}
        widget = {'nombre': forms.TextInput, 'estado':forms.CheckboxInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control', 'autocomplete':'off'})
        # self.fields['estado'].widget.attrs.update({'class':'form-control custom-file-input'})


# formulario para Ingreso
class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingresos
        fields = ['paciente','monto','detalle','fecha','tipo_pago' ,'estado']
    
        widget = {'nombre': forms.TextInput, 'estado':forms.CheckboxInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control', 'autocomplete':'off'})
        # self.fields['estado'].widget.attrs.update({'class':'form-control custom-file-input'})


class EgresoForm(forms.ModelForm):
    class Meta:
        model = Egresos
        fields = ['monto','detalle','fecha','num_factura' ,'estado', 'tipo_pago', 'detalle_state']
    
        widget = {'nombre': forms.TextInput, 'estado':forms.CheckboxInput, 'fecha':forms.DateInput,'detalle_state':forms.CheckboxInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control', 'autocomplete':'off'})
        self.fields['estado'].widget.attrs.update({'class':'form-check-input'})
        self.fields['detalle_state'].widget.attrs.update({'class':'form-check-input'})



