
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import DetailsListView, ProcessPayment,paytmresponse


urlpatterns = [
    
  
    path('details/<id>',DetailsListView.as_view(),name="details"),
    path('process/<order>/',ProcessPayment.as_view(),name="process"),
    path('response/',paytmresponse,name="response"),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

