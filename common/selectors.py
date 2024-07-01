from datetime import date
from django.utils.timezone import make_aware
from django.utils import timezone
from django.core.serializers import serialize

from companies.models import CierreCaja
from productos.models import Producto


def get_today_close(company):
    today = date.today()
    start_of_day = make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
    end_of_day = make_aware(timezone.datetime.combine(today, timezone.datetime.max.time()))

    cierre_exists = CierreCaja.objects.filter(
        compania_id=company,
        fecha__range=(start_of_day, end_of_day)
    ).exists()

    return cierre_exists


def get_company_products(user):
    compania = user.company_profile
    products = Producto.objects.filter(compania=compania)
    products_json = serialize('json', products)
    return products_json
