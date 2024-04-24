import calendar

from datetime import date
from datetime import datetime, timedelta
from django.db.models import Sum

from . import models as m
from clientes.models import ClienteProfile
from common.services import send_mms, send_payment_notify, send_credit_notify


def get_sales_month(user):
    hoy = datetime.today()
    primer_dia_mes_actual = hoy.replace(day=1)
    primer_dia_mes_pasado = primer_dia_mes_actual - timedelta(days=1)
    primer_dia_mes_pasado = primer_dia_mes_pasado.replace(day=1)

    sales_last_month = m.Transaccion.objects.filter(
        creada_por__company_profile=user.company_profile,
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
        creada_por__company_profile=user.company_profile,
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


def get_all_year_sales(user):
    hoy = datetime.today()

    ventas_mensuales = []

    for mes in range(1, 13):
        primer_dia_mes = hoy.replace(day=1, month=mes)
        _, ultimo_dia_mes = calendar.monthrange(hoy.year, mes)
        ultimo_dia_mes = hoy.replace(day=ultimo_dia_mes, month=mes)

        ventas_mes = m.Transaccion.objects.filter(
            creada_por__company_profile=user.company_profile,
            fecha_transaccion__gte=primer_dia_mes,
            fecha_transaccion__lt=ultimo_dia_mes,
            tipo_transaccion=m.Transaccion.TIPO_CHOICES[0][0]
        )

        if ventas_mes:
            total_this_year = ventas_mes.aggregate(
                total=Sum('total_transaccion')
            )
            total = int(total_this_year['total'])
            ventas_mensuales.append(total)
        else:
            ventas_mensuales.append(0)

    return ventas_mensuales


def get_sales_today(user):
    hoy = date.today()

    sales_today = m.Transaccion.objects.filter(
        creada_por__company_profile=user.company_profile,
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
        creada_por__company_profile=user.company_profile,
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
    total = m.Transaccion.objects.filter(
        cliente=cliente_profile
    ).aggregate(Sum('total_transaccion'))
    total = total['total_transaccion__sum'] or 0
    formatted_total = f'{total:,.0f}'
    return formatted_total


def get_cliente(id):
    cliente = ClienteProfile.objects.get(id=id)
    return cliente


def add_new_payment(form, cliente, user):
    form.instance.cliente = cliente
    form.instance.observaciones = m.Transaccion.TIPO_CHOICES[1][0]
    form.instance.tipo_transaccion = m.Transaccion.TIPO_CHOICES[1][0]
    form.instance.es_fiado = False
    form.instance.total_transaccion = form.instance.total_transaccion * -1
    form.instance.creada_por = user
    form.save()

    update_credit_balance(cliente, form.instance.total_transaccion)
    notify_payment_sms(cliente, cliente.deuda)
    send_payment_notify(
        user,
        cliente.telefono,
        f'{cliente.nombre} {cliente.apellido}',
        cliente.deuda
    )


def add_new_credit(form, cliente, user):
    form.instance.cliente = cliente
    form.instance.tipo_transaccion = m.Transaccion.TIPO_CHOICES[0][0]
    form.instance.es_fiado = True
    form.instance.total_transaccion = form.instance.total_transaccion
    form.instance.creada_por = user
    form.save()

    update_credit_balance(cliente, form.instance.total_transaccion)
    # notify_credit_sms(cliente, cliente.deuda)
    send_credit_notify(
        user,
        cliente.telefono,
        f'{cliente.nombre} {cliente.apellido}',
        cliente.deuda
    )


def update_credit_balance(cliente, total):
    last_balance = float(
        cliente.credit_balance
    ) if cliente.credit_balance else 0
    cliente.credit_balance = last_balance + float(total)
    cliente.save()


def notify_payment_sms(cliente, deuda):
    tel = ''.join(filter(str.isdigit, cliente.telefono))
    name = str(cliente).title().replace('App', '')

    body = f"""
¡Hola {name}!

¡Pago Realizado!

RESTANTE POR PAGAR:
${deuda}

Agropecuaria Donde Juancho
    """

    send_mms(tel, body)


def notify_credit_sms(cliente, deuda):
    tel = ''.join(filter(str.isdigit, cliente.telefono))
    name = str(cliente).title().replace('App', '')

    body = f"""
¡Hola {name}!

¡Credito Registrado!

DEUDA TOTAL:
${deuda}

Agropecuaria Donde Juancho
    """

    send_mms(tel, body)


def update_last_credit(cliente_profile, new_total, form):

    last = m.Transaccion.objects.filter(
        cliente=cliente_profile
    ).last()

    prev_balance = (
        int(cliente_profile.credit_balance) - int(last.total_transaccion)
    )

    last.observaciones = form.instance.observaciones
    last.total_transaccion = new_total
    last.save()

    cliente_profile.credit_balance = prev_balance + new_total
    cliente_profile.save()


def update_last_payment(cliente_profile, new_total, form):

    last = m.Transaccion.objects.filter(
        cliente=cliente_profile
    ).last()

    prev_balance = (
        int(cliente_profile.credit_balance) + (int(last.total_transaccion)*-1)
    )

    last.total_transaccion = new_total*-1
    last.save()

    cliente_profile.credit_balance = prev_balance - new_total
    cliente_profile.save()


def update_last_transaction(new_total, form, id):

    last = m.Transaccion.objects.filter(id=id).last()
    last.total_transaccion = new_total
    last.save()


def delete_last_transaction(id):
    last = m.Transaccion.objects.filter(id=id).last()
    last.delete()


def total_credit_amount(company):
    clientes = ClienteProfile.objects.filter(company=company)

    if clientes:
        total_today = clientes.aggregate(total=Sum('credit_balance'))
        total = total_today['total']
        formatted_total = f'{total:,.0f}'
        return formatted_total

    return 0
