
from datetime import date
from datetime import datetime, timedelta
from django.db.models import Sum

from . import models as m


def get_sales_month(user):
    hoy = datetime.today()
    primer_dia_mes_actual = hoy.replace(day=1)
    primer_dia_mes_pasado = primer_dia_mes_actual - timedelta(days=1)
    primer_dia_mes_pasado = primer_dia_mes_pasado.replace(day=1)

    sales_last_month = m.Venta.objects.filter(
        usuario__company_profile=user.company_profile,
        fecha_venta__gte=primer_dia_mes_actual,
        fecha_venta__lt=hoy
    )

    if sales_last_month:
        total_this_month = sales_last_month.aggregate(total=Sum('total_venta'))
        total = int(total_this_month['total'])
        formatted_total = f'{total:,.0f}'
        return formatted_total

    return 0

def get_sales_year(user):
    hoy = datetime.today()
    primer_dia_ano_actual = hoy.replace(day=1, month=1)

    sales_this_year = m.Venta.objects.filter(
        usuario__company_profile=user.company_profile,
        fecha_venta__gte=primer_dia_ano_actual,
        fecha_venta__lte=hoy
    )

    if sales_this_year:
        total_this_year = sales_this_year.aggregate(total=Sum('total_venta'))
        total = int(total_this_year['total'])
        formatted_total = f'{total:,.0f}'

        return formatted_total

    return 0


def get_sales_today(user):
    hoy = date.today()

    sales_today = m.Venta.objects.filter(
        usuario__company_profile=user.company_profile,
        fecha_venta__date=hoy
    )

    if sales_today:
        total_today = sales_today.aggregate(total=Sum('total_venta'))
        total = total_today['total']

        formatted_total = f'{total:,.0f}'

        return formatted_total

    return 0
