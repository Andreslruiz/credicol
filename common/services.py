import datetime
import requests
import json
import base64


from transacciones import services as vnt_s


def send_daily_report(user):
    today = datetime.date.today()
    today_format = today.strftime("%d/%m/%Y")
    today_sales = vnt_s.get_sales_today(user)
    credit_sales_today = vnt_s.get_credit_sales_today(user)

    body = f"""
Hola Andres,

Resumen ventas hoy:

VENTAS: ${today_sales}
FIADOS: ${credit_sales_today}

Agropecuaria Donde Juancho 🐷🌱
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
        'Authorization': 'Basic ' + base64.b64encode(f"{'Caloaizar2023'}:{'Rbkz2010'}".encode()).decode()
    }

    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        print(response.text)
    except Exception:
        print('No fue posible enviar mensaje de texto a: ', to)
