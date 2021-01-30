from django.urls import path
from .views import Profile, Signup




urlpatterns = [
    path('profile/',Profile.as_view(),name="profile"),
    path('signup/',Signup.as_view(),name="signup")
]
