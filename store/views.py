
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store.models import *
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import ListView

# Create your views here.

def home(request):
    return render(
        request,
        "store/home.html",
        {}
    )
class menList(ListView):
    model=Product
    fields="__all__"
    context_object_name='prod'
    template_name='store/men.html'
    paginate_by=3

@login_required
def cart(request):

    customer=request.user.customer 
    print("customer-------",customer)
    customer_data=Customer.objects.filter(name=customer)
    customer_id=customer_data[0].id
    print("customer_id-------",customer_id)
    order,created=Order.objects.get_or_create(customer_id=customer_id,ordered=False)
    
    items=order.orderitem_set.all()
    #order_id=orders[0].id
    #print("orders-------",orders)
    #order_items=Orderitem.objects.filter(order_id=order_id)
    #print("order_items-------",order_items[0].product.name,order_items[0].product.price)
    context={'data':items,'order':order}  
    return render(
        request,
        'store/cart.html',
        context
    )
    
    
@login_required
def checkout(request):
    customer=request.user.customer 
    print("customer-------",customer)
    customer_data=Customer.objects.filter(name=customer)
    customer_id=customer_data[0].id
    print("customer_id-------",customer_id)
    order,created=Order.objects.get_or_create(customer_id=customer_id,ordered=False)
    items=order.orderitem_set.all()
    context={'data':items,'order':order}
    return render(
        request,
        'store/checkout.html',
        context
    )

@login_required

def shippingaddress(request):
    cust=Customer.objects.get(name=request.user),
    order=Order.objects.get(customer=cust[0].id,ordered=False)
    if request.method=='POST':
        
        #foreign key value is not given yet
        ShippingAddress.objects.get_or_create(
            Customer_id=cust[0].id,
            order_id=order.id,
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            zipcode=request.POST.get('zipcode')
            
        )
        context={'order': order ,'customer':cust[0].name}
        return render(
            request,
            'details.html',
            context
        )
    else:
        return render(
            request,
            'store/checkout.html',
            {}
        )

@login_required
def add_to_cart(request,slug):
    print("slug=======",slug)
    customer=request.user.customer 
    customer_data=Customer.objects.filter(name=customer)
    customer_id=customer_data[0].id
     
    product = get_object_or_404(Product, slug=slug)
    
    print("product==============",product)
    print("customer===========",customer_data)
    ####
    order_qs = Order.objects.get_or_create(customer_id=customer_id, ordered=False) #check customer order 
    print("order_qs===========",order_qs[0].id)
    
    order_item, created = Orderitem.objects.get_or_create(
        product_id=product.id,
        order_id=order_qs[0].id,        
    )
    print("order_item===========",order_item)
    if order_qs:
        order = order_qs[0]
        # check if the order item is in the order
        if Orderitem.objects.filter(product_id=product.id):
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("men")
        else:
            Order.product.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("men")
        
    else:
        date_ordered = timezone.now()
        order = Order.objects.create(
            customer_id=customer_id,date_ordered=date_ordered)
        order.Product.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("men")
      
  