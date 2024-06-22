from django import forms

from . import models as m


class AddNewProducto(forms.ModelForm):

    class Meta:
        model = m.Producto
        fields = [
            'nombre',
            'precio',
            'iva',
            'costo_flete',
            'porcentaje_ganancia',
            'stock',
            'descripcion',
            'precio_venta'
        ]

        widgets = {
            'descripcion': forms.Textarea(attrs={'style': 'height:100px;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].label = ''
        self.fields['precio'].label = ''
        self.fields['stock'].label = ''
        self.fields['descripcion'].label = ''
        self.fields['iva'].label = ''
        self.fields['costo_flete'].label = ''
        self.fields['porcentaje_ganancia'].label = ''
        self.fields['precio_venta'].label = ''

        for field_name, field in self.fields.items():
            field.required = True

    def save(self, user, commit=True):
        producto = super().save(commit=False)
        producto.creado_por = user

        if commit:
            producto.save()

        return producto

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if m.Producto.objects.filter(nombre=nombre).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Ya existe este nombre de producto')
        return nombre
