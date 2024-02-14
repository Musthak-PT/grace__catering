from django.urls import path, re_path, include
from . import views

urlpatterns = [       
   re_path(r'^web/', include([
       
      path('get-room-booked-customer-details-excel-download', views.GetBookedCustomerDetailsExcelDownloadAPIView.as_view()),
      
   ])),
]