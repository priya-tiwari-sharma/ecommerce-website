from django.contrib.auth.decorators import login_required
from store.views import shippingaddress
from django.views.generic.list import ListView
from store.models import Customer, Order, Orderitem, ShippingAddress
from django.shortcuts import render

from django.views.generic import View
from random import randint
from paytm.Checksum import generate_checksum
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class DetailsListView(ListView):
    model = ShippingAddress
    template_name = "details.html"
    context_object_name = "shippingaddress"

class ProcessPayment(View):
    MERCHANT_KEY = 'bQfzzkKzeCbR7jOl'
    
    def get(self,request,order):
        
        order =Order.objects.get(id=order)
        amount = order.get_cart_total
        print("hello======get request",order,amount)
        param_dict = {
            'MID': 'amitgo59443067266036',
            'ORDER_ID': str(randint(111111,999999)), # order id 
            'TXN_AMOUNT': str(amount), # amount demanded for.
            'CUST_ID': "priyatiwari9424@gmail.com",
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEB', # for demo purpose only.
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/payment/response/' # on this url paytm will send you the status of request
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
    """
    customer=request.user.customer
    print("customer====",customer)
    customer_data=Customer.objects.filter(name=customer)
    print("customer_data====",customer_data)
    customer_id=customer_data[0].id
    print("custome_id====",customer_id)
    order_qs = Order.objects.get(customer_id=customer_id, ordered=False) #check customer order 
    print("order_qs====",order_qs)
    order_qs.ordered=True
    order_qs.save()

    orderitem=Orderitem.objects.get(order_id=order_qs,ordered=False)
    orderitem.ordered=True
    orderitem.save()
    print("orderitem=======",orderitem)
    """
    return render(
        request,
        "info.html",
        {
            "data":request.POST
        }
    )