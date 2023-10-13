from django import forms
from . import models as m


class CrearVentaForm(forms.ModelForm):

    class Meta:
        model = m.Transaccion
        fields = [
            'tipo_transaccion',
            'usuario',
            'total_transaccion',
            'es_fiado',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['total_transaccion'].label = 'Total Venta'
        self.fields['es_fiado'].label = 'Es Fiado'
