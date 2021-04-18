from django import forms

from .models import Unidad_medida, Item, Marca, Doc_ingreso, Doc_salida


class Unidad_medidaForm(forms.ModelForm):
    class Meta:
        model = Unidad_medida
        fields = ['nombre','abreviacion','detalle','estado']
        labels = {'nombre':'Nombre','abreviacion':'Abreviación','detalle':'Detalle','estado':'Estado'}
        widget = {'nombre': forms.TextInput, 'estado':forms.CheckboxInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control', 'autocomplete':'off'})
        # self.fields['estado'].widget.attrs.update({'class':'form-control custom-file-input'})


class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre','detalle','estado']
        labels = {'nombre':'Nombre','detalle':'Detalle','estado':'Estado'}
        widget = {'nombre': forms.TextInput, 'estado':forms.CheckboxInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control', 'autocomplete':'off'})
        # self.fields['estado'].widget.attrs.update({'class':'form-control custom-file-input'})

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['nombre','marca','detalle','codigo','unidad_medida_basica','cantidad','cantidad_minima','cantidad_maxima','factor_conversion','estado']
        labels = {'nombre':'Nombre','marca':'Marca','detalle':'Detalle','codigo':'Codigo','unidad_medida_basica':'Unidad de medida basica','cantidad':'Cantidad','cantidad_minima':'Cantidad minima','cantidad_maxima':'Cantidad Maxima','factor_conversion':'Factor de Conversión','estado':'Estado'}
#         widget = {'nombre': forms.TextInput, 'estado':forms.CheckboxInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control', 'autocomplete':'off'})
        # self.fields['estado'].widget.attrs.update({'class':'form-control custom-file-input'})


class Doc_ingresoForm(forms.ModelForm):
    class Meta:
        model = Doc_ingreso
        fields = ['fecha','razon',]
        labels = {'fecha':'Fecha','razon':'Razon'}
#         widget = {'nombre': forms.TextInput, 'estado':forms.CheckboxInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control', 'autocomplete':'off'})
        # self.fields['estado'].widget.attrs.update({'class':'form-control custom-file-input'})


class Doc_salidaForm(forms.ModelForm):
    class Meta:
        model = Doc_salida
        fields = ['fecha','razon',]
        labels = {'fecha':'Fecha','razon':'Razon'}
#         widget = {'nombre': forms.TextInput, 'estado':forms.CheckboxInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control', 'autocomplete':'off'})
        # self.fields['estado'].widget.attrs.update({'class':'form-control custom-file-input'})