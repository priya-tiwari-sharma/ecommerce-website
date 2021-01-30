from django.shortcuts import render
from django.contrib.auth.models import User
from store.models import *
from .forms import SignupForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    View,
    TemplateView
)
# Create your views here.


class Profile(LoginRequiredMixin,View):
    login_url = "/auth/login/"
    def get(self,request):
        return render(                      
            request,
            "store/home.html",
            {
                'title':request.user.first_name
            }
        )
    def post(self,request):pass

class Signup(View):
    def get(self,request):
        return render(
            request,
            "signup.html",
            {
                'title':'Sign-Up Page',
                'form':SignupForm(None)
            }
        )
    def post(self,request):
        form = SignupForm(request.POST)
        if form.is_valid():       
            form.save()
            user = User.objects.get(username=request.POST['username'])
            user.set_password(request.POST['password'])
            user.save()
            customer=Customer.objects.create(user=user,name=request.POST['username'],email=request.POST['email'])
            customer.save()
        return render(
            request,
            "signup.html",
            {
                'title':'Sign-Up Page',
                'form':SignupForm(None),
                'msg':'Signup successfully!'
            }
        )

