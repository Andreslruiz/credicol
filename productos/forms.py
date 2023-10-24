from django import forms

from . import models as m


class AddNewProducto(forms.ModelForm):

    class Meta:
        model = m.Producto
        fields = [
            'nombre',
            'precio',
            'stock',
            'descripcion'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].label = ''
        self.fields['precio'].label = ''
        self.fields['stock'].label = ''
        self.fields['descripcion'].label = ''

        for field_name, field in self.fields.items():
            field.required = True
