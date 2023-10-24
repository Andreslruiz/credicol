# import datetime
import requests
import json
import base64


from transacciones import services as vnt_s
from . import models as m


def send_daily_report(user):
    today_sales = vnt_s.get_sales_today(user)
    credit_sales_today = vnt_s.get_credit_sales_today(user)

    body = f"""
¡Hola {user.company_profile}!

Resumen ventas hoy:

VENTAS: ${today_sales}
FIADOS: ${credit_sales_today}

Agropecuaria Donde Juancho
    """

    send_mms('573213358263', body)


def send_mms(to, body):

    data = {
        'to': ['573213358263'],
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

    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code not in [200, 202]:
            add_pending_msg(to, body, response.text)

    except Exception as e:
        add_pending_msg(to, body, e)


def add_pending_msg(to, message, error_code):
    new_msg = m.PendingMsgView.objects.create(
        text=message, error_code=error_code,
        to=to
    )

    new_msg.save()


def send_payment_notify(to, username, balance):
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
            "name": "send_notify",
            "language": {
                "code": "en_US"
            },
            # "components": [
            #     {
            #         "type": "text",
            #         "parameters": [
            #             {
            #                 "type": "text",
            #                 "text": username
            #             },
            #             {
            #                 "type": "text",
            #                 "text": balance
            #             }
            #         ]
            #     }
            # ]
        }
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.text)
