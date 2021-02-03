
from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import add_to_cart, checkout, home, menList,cart, shippingaddress

urlpatterns = [
  
    path('',home,name="home"),
    path('men/',login_required(menList.as_view()),name="men"),
    path('cart/',cart,name="cart"),
    path('checkout/',checkout,name="checkout"),
    path('shippingaddress/',shippingaddress,name='shippingaddress'),
    
    path('add_to_cart/<slug>/',add_to_cart,name="add_to_cart"),
   
   
]
    