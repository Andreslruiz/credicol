from django import forms

from . import models as m


class CrearGastoForm(forms.ModelForm):

    class Meta:
        model = m.Gasto
        fields = [
            'creada_por',
            'total_gasto',
            'observaciones',
            'company'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['observaciones'].label = ''
        self.fields['total_gasto'].label = ''
