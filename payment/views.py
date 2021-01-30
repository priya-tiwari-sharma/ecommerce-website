from store.models import Order
from django.shortcuts import render

from django.views.generic import View
from random import randint
from paytm.Checksum import generate_checksum
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


class ProcessPayment(View):
    MERCHANT_KEY = 'bQfzzkKzeCbR7jOl'
    def get(self,request,pk):
        product = Order.get_cart_total
        param_dict = {
            'MID': 'amitgo59443067266036',
            'ORDER_ID': str(randint(111111,999999)), # order id 
            'TXN_AMOUNT': str(product), # amount demanded for.
            'CUST_ID': "mailtomeontushar@gmail.com",
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEB', # for demo purpose only.
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/response/' # on this url paytm will send you the status of request
        }
        param_dict['CHECKSUMHASH'] = generate_checksum(param_dict,ProcessPayment.MERCHANT_KEY)
        return render(
            request,
            "process.html",
            {
                "data":param_dict
            }
        )

    def post(self,request):pass

@csrf_exempt
def paytmresponse(request):
    return render(
        request,
        "info.html",
        {
            "data":request.POST
        }
    )