from django import forms

from . import models as m


class AddNewReport(forms.ModelForm):

    ciudad = forms.CharField(max_length=255, required=True)
    cliente = forms.CharField(max_length=255, required=True)

    class Meta:
        model = m.Reporte
        fields = [
            'ciudad',
            'cliente',
            'tipo_reporte'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.required = True
            field.label = ''

    def save(self, user, commit=True):
        producto = super().save(commit=False)
        producto.tecnico = user

        if commit:
            producto.save()

        return producto


class AddNewEmpleado(forms.ModelForm):

    class Meta:
        model = m.Empleado
        fields = [
            'nombre',
            'apellido',
            'telefono',
            'puesto'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.required = True
            field.label = ''

    def save(self, user, commit=True):
        empleado = super().save(commit=False)
        empleado.user = user

        if commit:
            empleado.save()

        return empleado


class EditEmpleado(forms.ModelForm):

    class Meta:
        model = m.Empleado
        fields = [
            'nombre',
            'apellido',
            'telefono',
            'puesto'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.required = True
            field.label = ''
