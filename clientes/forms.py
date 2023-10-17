from django import forms

from . import models as m


class AddNewCliente(forms.ModelForm):

    class Meta:
        model = m.ClienteProfile
        fields = [
            'nombre',
            'apellido',
            'email',
            'telefono'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].label = ''
        self.fields['apellido'].label = ''
        self.fields['email'].label = ''
        self.fields['telefono'].label = ''

        for field_name, field in self.fields.items():
            field.required = True
