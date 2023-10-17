from django import forms

from . import models as m
from . import services as s

class CrearVentaForm(forms.ModelForm):

    class Meta:
        model = m.Transaccion
        fields = [
            'tipo_transaccion',
            'creada_por',
            'total_transaccion',
            'es_fiado',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['total_transaccion'].label = 'Total Venta'
        self.fields['es_fiado'].label = 'Es Fiado'


class AddPaymentForm(forms.ModelForm):

    class Meta:
        model = m.Transaccion
        fields = [
            'cliente',
            'tipo_transaccion',
            'es_fiado',
            'total_transaccion'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['total_transaccion'].label = ''


class AddCreditForm(forms.ModelForm):

    class Meta:
        model = m.Transaccion
        fields = [
            'cliente',
            'tipo_transaccion',
            'es_fiado',
            'total_transaccion',
            'observaciones'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['total_transaccion'].label = ''
        self.fields['observaciones'].label = ''
        self.fields['observaciones'].required = True
