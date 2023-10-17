import requests

from datetime import date
from datetime import datetime, timedelta
from django.db.models import Sum

from . import models as m
from clientes.models import ClienteProfile


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
    total = m.Transaccion.objects.filter(cliente=cliente_profile).aggregate(Sum('total_transaccion'))
    total = total['total_transaccion__sum'] or 0
    formatted_total = f'{total:,.0f}'
    return formatted_total


def get_cliente(id):
    cliente = ClienteProfile.objects.get(id=id)
    return cliente


def add_new_payment(form, cliente, user):
    form.instance.cliente = cliente
    form.instance.tipo_transaccion = m.Transaccion.TIPO_CHOICES[1][0]
    form.instance.es_fiado = False
    form.instance.total_transaccion = form.instance.total_transaccion * -1
    form.instance.creada_por = user
    form.save()

    update_credit_balance(cliente, form.instance.total_transaccion)


def add_new_credit(form, cliente, user):
    form.instance.cliente = cliente
    form.instance.tipo_transaccion = m.Transaccion.TIPO_CHOICES[0][0]
    form.instance.es_fiado = True
    form.instance.total_transaccion = form.instance.total_transaccion
    form.instance.creada_por = user
    form.save()

    update_credit_balance(cliente, form.instance.total_transaccion)


def update_credit_balance(cliente, total):
    cliente.credit_balance = float(cliente.credit_balance) + float(total)
    cliente.save()


def send_wspp_message():
    token = "EAAJqf41ZCOq8BOZBnBblyYr40ouXRSPhz9ZCljH656tfBpWjWItUyUwYVbWTVveZB7cEZBMGyhLXVZByLuhIUyxVgZBuTwMbAc3KuJ541aToLzJyONn2BlbL5uqGLwU8a1QcYMISfAt6Hd7c5sZCxSDGrriejUsSe1oxL3KQH4rUYO2RLOn2nFVVOUMsRNLoPCg0V8t1s7rPM5ZCxSdCmJBMBgx8li8AldjxlNAZDZD"
    url = "https://graph.facebook.com/v17.0/142793695585950/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": "573213358263",
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {
                "code": "en_US"
            },
            # "components": [
            #     {
            #         "type": "body",
            #         "parameters": [
            #             {
            #                 "type": "text",
            #                 "text": "Tu valor para {{1}}"
            #             }
            #         ]
            #     },
            #     {
            #         "type": "body",
            #         "parameters": [
            #             {
            #                 "type": "text",
            #                 "text": "Tu valor para {{2}}"
            #             }
            #         ]
            #     }
            # ]
        }
    }

    requests.post(url, json=data, headers=headers)
