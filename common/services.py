import datetime
import requests


from transacciones import services as vnt_s


def send_daily_report(user):
    today = datetime.date.today()
    today_format = today.strftime("%d/%m/%Y")
    today_sales = vnt_s.get_sales_today(user)
    credit_sales_today = vnt_s.get_credit_sales_today(user)

    body = f"""
¡Hola Carlos Andres Loaiza!

✅ Detalle de tus ventas - {today_format}

TOTAL VENTAS HOY:
${today_sales}

TOTAL FIADOS HOY:
${credit_sales_today}

Saludos cordiales, Agropecuaria Donde Juancho 🐷🌱

Sistema de facturación, registro DIAN Colombia REG2023736
    """

    send_mms('573213358263', body)


def send_mms(tel, body):
    tel = f'57{tel}'
    url = "http://api.messaging-service.com/sms/1/text/single"

    payload = {
        "from": "Agropecuaria Donde Juancho",
        "to": ["573213358263"],
        "text": body
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Basic QVBJQ29sb21iaWFyZWQ6MTAwJUNvbG9tYmlhcmVk"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response)
