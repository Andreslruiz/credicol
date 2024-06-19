# import datetime
import requests
import json
import base64

from django.utils import timezone
from transacciones import services as vnt_s
from . import models as m


def send_daily_report(user):
    today_sales = vnt_s.get_sales_today(user)
    credit_sales = vnt_s.get_credit_sales_today(user)

    body = f"""
¡Hola {user.company_profile}!

Resumen ventas hoy:

VENTAS: ${today_sales}
FIADOS: ${credit_sales}

Agropecuaria Donde Juancho
    """
    send_daily_report_wspp(
        user.company_profile, today_sales, credit_sales
    )
    # send_mms('573213358263', body)



def send_mms(to, body):
    to = f'57{to}'
    data = {
        'to': [to],
        'text': body,
        'from': 'Agrop'
    }

    url = 'https://Smsmasivos.colombiared.com.co/Api/rest/message'

    headers = {
        'Accept': 'application/json',
        'Authorization': (
            'Basic ' + base64.b64encode(
                f"{'Caloaizar2023'}:{'Rbkz2010'}".encode()
            ).decode()
        )
    }

    data = json.dumps(data)

    try:
        requests.post(url, data=data, headers=headers)
    except Exception as e:
        add_pending_msg(url, data, headers, e)


def add_pending_msg(url, data, headers, error):
    new_msg = m.PendingMsgView.objects.create(
        url=url, data=data,
        headers=headers, type=m.PendingMsgView.MSG,
        error_code=error
    )

    new_msg.save()


def add_pending_wspp_msg(url, data, headers, error):
    new_msg = m.PendingMsgView.objects.create(
        url=url, data=data,
        headers=headers, type=m.PendingMsgView.WS,
        error_code=error
    )

    new_msg.save()


def send_payment_notify(user, to, username, balance):
    company = user.company_profile
    if company.fin_fecha_membresia < timezone.now() or not company.envio_mensajes:
        return True
    url = "https://graph.facebook.com/v17.0/142793695585950/messages"

    headers = {
        "Authorization": "Bearer EAAJqf41ZCOq8BO6zSZBwJP624ZAJhKXTmry9ktawZA2VfFXreiuQ07OMQwZBcgR9ZCuY1zgfKpB4fdqOyfspJK0UXGvp3o3OCSJlZCwd4QMlrAb69hBN8S7evmr2Vont84jZAO91QfZBWr3B96RkTAcmEVWMVAtqIgCDDYUuSNUMUxKw6DE91vYP9JVuxyACRePaaqeP2oeP94rzbclHx",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": f"+57{to}",
        "type": "template",
        "template": {
            "name": "pago",
            "language": {
                "code": "en_US"
            },
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "text",
                            "text": username.title()
                        }
                    ]
                },
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": balance
                        }
                    ]
                }
            ]
        }
    }

    try:
        requests.post(url, headers=headers, json=data)
    except Exception:
        add_pending_wspp_msg(url, data, headers)


def send_credit_notify(user, to, username, balance):
    company = user.company_profile
    if company.fin_fecha_membresia < timezone.now() or not company.envio_mensajes:
        return True

    url = "https://graph.facebook.com/v17.0/142793695585950/messages"

    headers = {
        "Authorization": "Bearer EAAJqf41ZCOq8BO6zSZBwJP624ZAJhKXTmry9ktawZA2VfFXreiuQ07OMQwZBcgR9ZCuY1zgfKpB4fdqOyfspJK0UXGvp3o3OCSJlZCwd4QMlrAb69hBN8S7evmr2Vont84jZAO91QfZBWr3B96RkTAcmEVWMVAtqIgCDDYUuSNUMUxKw6DE91vYP9JVuxyACRePaaqeP2oeP94rzbclHx",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": f"+57{to}",
        "type": "template",
        "template": {
            "name": "credito",
            "language": {
                "code": "en_US"
            },
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "text",
                            "text": username.title()
                        }
                    ]
                },
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": balance
                        }
                    ]
                }
            ]
        }
    }

    try:
        requests.post(url, headers=headers, json=data)
    except Exception as e:
        add_pending_wspp_msg(url, data, headers, e)


def send_daily_report_wspp(
        company, today_sales, credit_sales
    ):
    url = "https://graph.facebook.com/v17.0/142793695585950/messages"

    headers = {
        "Authorization": "Bearer EAAJqf41ZCOq8BO6zSZBwJP624ZAJhKXTmry9ktawZA2VfFXreiuQ07OMQwZBcgR9ZCuY1zgfKpB4fdqOyfspJK0UXGvp3o3OCSJlZCwd4QMlrAb69hBN8S7evmr2Vont84jZAO91QfZBWr3B96RkTAcmEVWMVAtqIgCDDYUuSNUMUxKw6DE91vYP9JVuxyACRePaaqeP2oeP94rzbclHx",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": "+573213358263",
        "type": "template",
        "template": {
            "name": "daily_report",
            "language": {
                "code": "en_US"
            },
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "text",
                            "text": company.name.title()
                        }
                    ]
                },
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": today_sales
                        }
                    ],
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": credit_sales
                        }
                    ]
                }
            ]
        }
    }

    try:
        requests.post(url, headers=headers, json=data)
    except Exception as e:
        add_pending_wspp_msg(url, data, headers, e)
