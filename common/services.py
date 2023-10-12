from twilio.rest import Client


def send_daily_notification():
    account_sid = 'AC06a3a8497607833c786dab56d20f5eec'
    auth_token = 'b256f84383b1cf0b0cd7c1f5d672ba7b'
    client = Client(account_sid, auth_token)

    message=client.messages.create(
    from_='whatsapp:+14155238886',
    body='Your appointment is coming up on July 21 at 3PM',
    to='whatsapp:+573213358263'
    )

    print(message)
