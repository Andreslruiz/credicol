
from datetime import date
from datetime import datetime, timedelta
from django.db.models import Sum

from . import models as m


def get_sales_month(user):
    hoy = datetime.today()
    primer_dia_mes_actual = hoy.replace(day=1)
    primer_dia_mes_pasado = primer_dia_mes_actual - timedelta(days=1)
    primer_dia_mes_pasado = primer_dia_mes_pasado.replace(day=1)

    sales_last_month = m.Transaccion.objects.filter(
        usuario__company_profile=user.company_profile,
        fecha_transaccion__gte=primer_dia_mes_actual,
        fecha_transaccion__lt=hoy,
        tipo_transaccion=m.Transaccion.TIPO_CHOICES[0][0]
    )

    if sales_last_month:
        total_this_month = sales_last_month.aggregate(
            total=Sum('total_transaccion')
        )
        total = int(total_this_month['total'])
        formatted_total = f'{total:,.0f}'
        return formatted_total

    return 0


def get_sales_year(user):
    hoy = datetime.today()
    primer_dia_ano_actual = hoy.replace(day=1, month=1)

    sales_this_year = m.Transaccion.objects.filter(
        usuario__company_profile=user.company_profile,
        fecha_transaccion__gte=primer_dia_ano_actual,
        fecha_transaccion__lte=hoy,
        tipo_transaccion=m.Transaccion.TIPO_CHOICES[0][0]
    )

    if sales_this_year:
        total_this_year = sales_this_year.aggregate(
            total=Sum('total_transaccion')
        )
        total = int(total_this_year['total'])
        formatted_total = f'{total:,.0f}'

        return formatted_total

    return 0


def get_sales_today(user):
    hoy = date.today()

    sales_today = m.Transaccion.objects.filter(
        usuario__company_profile=user.company_profile,
        fecha_transaccion__date=hoy,
        tipo_transaccion=m.Transaccion.TIPO_CHOICES[0][0]
    )

    if sales_today:
        total_today = sales_today.aggregate(total=Sum('total_transaccion'))
        total = total_today['total']
        formatted_total = f'{total:,.0f}'
        return formatted_total

    return 0


def get_credit_sales_today(user):
    hoy = date.today()

    sales_today = m.Transaccion.objects.filter(
        usuario__company_profile=user.company_profile,
        fecha_transaccion__date=hoy, es_fiado=True,
        tipo_transaccion=m.Transaccion.TIPO_CHOICES[0][0]
    )

    if sales_today:
        total_today = sales_today.aggregate(total=Sum('total_transaccion'))
        total = total_today['total']
        formatted_total = f'{total:,.0f}'
        return formatted_total

    return 0


def get_current_user_deuda(cliente_profile):
    total = m.Transaccion.objects.filter(cliente=cliente_profile).aggregate(Sum('total_transaccion'))
    total = total['total_transaccion__sum'] or 0
    formatted_total = f'{total:,.0f}'
    return formatted_total
