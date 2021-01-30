from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL
from django.db.models.signals import post_save  #signal
from django.core.mail import EmailMultiAlternatives #email html page
from django.template.loader import render_to_string
from django.urls import resolvers # render  html email text  
from django.utils.html import strip_tags # remove html tag 
from django.shortcuts import  reverse
from django.urls import resolve

#------------------------------------Models in database-------------------------------
# customer(user,name,email)
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.name

#product(name,price,digital)
class Product(models.Model):
    name=models.CharField(max_length=200,null=True)
    price=models.FloatField()
    image=models.ImageField(null=True,blank=True)
    
    slug=models.SlugField()
    
    def __str__(self):
        return str(self.name)
   
    
    def get_add_to_cart_url(self):
        print("hello=====================",self.slug)
        return reverse("add_to_cart", kwargs={
            'slug': self.slug
        })
   
    def get_remove_from_cart_url(self):
        return reverse("remove_from_cart", kwargs={
            'slug': self.slug
        })

#order(---customer---,date_ordered,complete,transaction_id)
class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    transaction_id=models.CharField(max_length=200,null=True)
    ordered=models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total

#orderitem(---product,order---,quantity,date_added)
class Orderitem(models.Model):
    product=models.ForeignKey(Product,on_delete=SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=SET_NULL,blank=True,null=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    ordered = models.BooleanField(default=False)
    date_added=models.DateTimeField(auto_now_add=True)
    @property
    def get_total(self):
        total=self.product.price * self.quantity
        return total
   


    def __str__(self):
            return str(self.product) +"-----------------"+ str(self.quantity)

#shippingaddress(---customer,order----,address,city,state,zipcode,date_added)
class ShippingAddress(models.Model):
    Customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=SET_NULL,blank=True,null=True)
    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(max_length=200,null=True)
    address=models.CharField(max_length=200,null=True)
    city=models.CharField(max_length=200,null=True)
    state=models.CharField(max_length=200,null=True)
    zipcode=models.CharField(max_length=200,null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address

###########################################################
#Signal-----FOR-------Send Email----------------

#add new product in website
def Product_Add_Signal(sender,instance,**kwargs):
    print("created=======",kwargs['created'])
    #for sending email
    if kwargs['created']:
        subject="New Item Added"
        to="sharma.ab21@gmail.com"
        from_email="priyatiwari9424@gmail.com"
        data = Product.objects.all().last()
        html_content=render_to_string(
            "store/email.html",
            {
                "data":data
            }
        )
        text_content=strip_tags(html_content)
        msg=EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            [to]
        )
        msg.attach_alternative(html_content,"text/html")
        msg.send()

   
post_save.connect(Product_Add_Signal,sender=Product)    



#sucessfully placed order
"""
def Bill_Generate_Signal(sender,instance,**kwargs):
    print("Your order has been placed successfully") 

post_save.connect(Bill_Generate_Signal,sender=Order)
"""

    




