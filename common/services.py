from twilio.rest import Client


def send_daily_notification(total_venta):
    account_sid = 'AC06a3a8497607833c786dab56d20f5eec'
    auth_token = '[AuthToken]'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='whatsapp:+14155238886',
    body=f'Acabas de vender: {total_venta}',
    to='whatsapp:+573213358263'
    )

    print(message.sid)
