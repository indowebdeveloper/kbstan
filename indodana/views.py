from django.shortcuts import render

from django.http import JsonResponse
from .models import Indodana

from orders.models import Order

def debug(request):

    # order = Order.objects.filter(shippingAddress__gt=0)
    order = Order.objects.last()

    # print(order)

    indodana = Indodana(order)
    resp_data = indodana.send_transaction_request()

    return JsonResponse(resp_data)