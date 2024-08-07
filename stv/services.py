from django.conf import settings
from datetime import datetime
from openpyxl import load_workbook


def create_new_report(instance, request):
    direccion = request.POST.get('direccion')
    administrador = request.POST.get('administrador')

    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    file_path = f'{settings.STATICFILES_DIRS[0]}/stv_files/formato_visita.xlsx'
    output_path = f'{settings.MEDIA_ROOT}/reportes/{instance.cliente.title()} - {fecha_hoy}.xlsx'

    wb = load_workbook(file_path)
    replace_name_reporte_xlsx(wb, file_path, f'input_{instance.tipo_reporte}', 'X')
    replace_name_reporte_xlsx(wb, file_path, 'input_cliente', instance.cliente.title())
    replace_name_reporte_xlsx(wb, file_path, 'input_ciudad', instance.ciudad)
    replace_name_reporte_xlsx(wb, file_path, 'input_direccion', direccion)
    replace_name_reporte_xlsx(wb, file_path, 'input_administrador', administrador)
    wb.save(output_path)

    instance.archivo.name = f'{instance.cliente.title()} - {fecha_hoy}.xlsx'
    instance.save()
    return instance


def replace_name_reporte_xlsx(wb, file_path, target_word, replacement_word):
    for sheet in wb.sheetnames:
        ws = wb[sheet]

        for row in ws.iter_rows():
            for cell in row:
                if isinstance(cell.value, str) and target_word in cell.value:
                    cell.value = cell.value.replace(target_word, replacement_word)
    return wb
