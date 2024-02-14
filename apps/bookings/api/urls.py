from django.urls import path, re_path, include
from . import views

urlpatterns = [       
   re_path(r'^web/', include([
      path('booking-confirmation-view', views.BookingConfirmationApiView.as_view()),
   ])),
]