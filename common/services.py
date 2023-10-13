import pyautogui
import webbrowser
import time
import datetime


from twilio.rest import Client
from transacciones import services as vnt_s


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


def send_daily_report(user):
    today = datetime.date.today()
    today_format = today.strftime("%d/%m/%Y")
    today_sales = vnt_s.get_sales_today(user)
    credit_sales_today = vnt_s.get_credit_sales_today(user)
    webbrowser.open('https://web.whatsapp.com/send?phone=+573213358263')
    time.sleep(15)
    pyautogui.typewrite(
        f"""*TOTAL SALES TODAY {today_format}*: {today_sales}, *TOTAL CREDIT SALES:* {credit_sales_today}"""
    )
    pyautogui.press("enter")
    time.sleep(2)
