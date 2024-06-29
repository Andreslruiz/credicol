import urllib.parse
import requests
from django.conf import settings


def send_payment_message(nombre_empresa, nombre_cliente, numero_cliente, nuevo_balance):

    recipient = f"+57{numero_cliente}"
    apikey = settings.WSSP_KEY
    name = nombre_cliente
    total = nuevo_balance
    company = nombre_empresa

    base_url = "https://api.textmebot.com/send.php"
    message_template = (
        "🚨 _*{company}*_\n\n"
        "¡Hola {name}!\n"
        "¡Pago Realizado! ✅ Queremos informarte amablemente que el valor restante de "
        "tus compras fiadas es de:\n\n"
        "*RESTANTE POR PAGAR:*\n"
        "*${total}*\n\n"
        "Un gusto atenderte.\n\n"
        "Saludos cordiales, {company}\n\n"
        "_CrediCol Colombia 2024_"
    )

    message = message_template.format(name=name, total=total, company=company)
    encoded_message = urllib.parse.quote(message)

    full_url = f"{base_url}?recipient={urllib.parse.quote(recipient)}&apikey={apikey}&text={encoded_message}"
    responde = requests.get(full_url)
    return responde

