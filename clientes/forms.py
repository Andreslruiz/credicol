from django import forms

from . import models as m


class AddNewCliente(forms.ModelForm):

    class Meta:
        model = m.ClienteProfile
        fields = [
            'nombre',
            'apellido',
            'email',
            'telefono',
            'credit_balance'
        ]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        self.fields['nombre'].label = ''
        self.fields['apellido'].label = ''
        self.fields['email'].label = ''
        self.fields['telefono'].label = ''
        self.fields['credit_balance'].label = ''

        self.fields['nombre'].required = True
        self.fields['apellido'].required = True

        if request and request.user.company_profile.envio_mensajes:
            self.fields['telefono'].required = True
