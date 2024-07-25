import urllib.parse
import requests

from django.conf import settings
from django.utils import timezone


def send_payment_notify(user, to, username, balance):
    company = user.company_profile
    if company.fin_fecha_membresia < timezone.now() or not company.envio_mensajes:
        return True

    recipient = f"+57{to}"
    apikey = settings.WSSP_KEY

    name = username.title()
    total = balance
    company = company.name.title()

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
    response = requests.get(full_url)
    return response.status_code == 200


def send_credit_notify(user, to, username, balance):
    company = user.company_profile
    if company.fin_fecha_membresia < timezone.now() or not company.envio_mensajes:
        return True

    recipient = f"+57{to}"
    apikey = settings.WSSP_KEY
    name = username.title()
    total = balance
    company_name = company.name.title()

    base_url = "https://api.textmebot.com/send.php"
    message_template = (
        "🚨 _*{company_name}*_\n\n"
        "¡Hola {name}!\n"
        "¡Compra Realizada! 📌 Queremos informarte amablemente que el valor restante de "
        "tus compras fiadas es de:\n\n"
        "*RESTANTE POR PAGAR:*\n"
        "*${total}*\n\n"
        "Un gusto atenderte.\n\n"
        "Saludos cordiales, {company_name}\n\n"
        "_CrediCol Colombia 2024_"
    )

    message = message_template.format(name=name, total=total, company_name=company_name)
    encoded_message = urllib.parse.quote(message)

    full_url = f"{base_url}?recipient={urllib.parse.quote(recipient)}&apikey={apikey}&text={encoded_message}&file={company.company_image_url}"
    response = requests.get(full_url)
    return response.status_code == 200


def remember_payment_notify(user, to, username, balance, days_overdue):
    company = user.company_profile
    if company.fin_fecha_membresia < timezone.now() or not company.envio_mensajes:
        return True

    recipient = f"+57{to}"
    apikey = settings.WSSP_KEY

    name = username.title()
    total = balance
    company_name = company.name.title()
    contact = company.contact

    base_url = "https://api.textmebot.com/send.php"
    message_template = (
        "¡Hola {name}!\n"
        "⚠️ Recordatorio de Pago\n\n"
        "Queremos informarte que tienes un saldo pendiente de ${total}.\n\n"
        "🗓️ Días en mora: {days_overdue} días\n\n"
        "Si tienes alguna duda contacta a la empresa al {contact}. Estamos aquí para ayudarte.\n\n"
        "Un cordial saludo,\n"
        "{company_name}\n\n"
        "_CrediCol Colombia 2024_\n"
    )

    message = message_template.format(name=name, total=total, contact=contact, days_overdue=days_overdue, company_name=company_name)
    encoded_message = urllib.parse.quote(message)

    full_url = f"{base_url}?recipient={urllib.parse.quote(recipient)}&apikey={apikey}&text={encoded_message}"
    response = requests.get(full_url)
    return response.status_code == 200


def send_payment_notify_old(user, to, username, balance):
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
        pass


def send_credit_notify_old(user, to, username, balance):
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
        pass


def send_cluster_test(recipient, message):
    apikey = settings.WSSP_KEY
    base_url = "https://api.textmebot.com/send.php"
    encoded_message = urllib.parse.quote(message)
    full_url = f"{base_url}?recipient={urllib.parse.quote(recipient)}&apikey={apikey}&text={encoded_message}"
    response = requests.get(full_url)
    return response.status_code == 200


def send_daily_summary(user, efectivo, gastos, comentarios, credits_today):
    company = user.company_profile
    prop_number = company.propietario.phone_number
    recipient = f"+57{prop_number}"
    apikey = settings.WSSP_KEY

    company_name = company.name.title()
    message_template = (
        "📊 *Resumen del Día* 📊\n\n"
        "🏢 Empresa: {company_name}\n\n"
        "💳 Total Créditos: ${total_credito}\n"
        "💵 Total Efectivo: ${total_efectivo}\n"
        "💸 Total Gastos: ${total_gastos}\n\n"
        "📝 Comentarios:\n{comentarios}\n\n"
        "¡Excelente trabajo hoy!\n\n"
        "CrediCol Colombia 2024\n"
    )

    message = message_template.format(
        company_name=company_name,
        total_credito=credits_today,
        total_efectivo=f'{int(efectivo):,.0f}',
        total_gastos=f'{int(gastos):,.0f}',
        comentarios=comentarios if comentarios else "Ninguno",
    )
    encoded_message = urllib.parse.quote(message)

    base_url = "https://api.textmebot.com/send.php"
    full_url = f"{base_url}?recipient={urllib.parse.quote(recipient)}&apikey={apikey}&text={encoded_message}"
    response = requests.get(full_url)
    return response.status_code == 200
