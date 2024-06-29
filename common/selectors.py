from datetime import date
from django.utils.timezone import make_aware
from django.utils import timezone

from companies.models import CierreCaja


def get_today_close(company):
    today = date.today()
    start_of_day = make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
    end_of_day = make_aware(timezone.datetime.combine(today, timezone.datetime.max.time()))

    cierre_exists = CierreCaja.objects.filter(
        compania_id=company,
        fecha__range=(start_of_day, end_of_day)
    ).exists()

    return cierre_exists
