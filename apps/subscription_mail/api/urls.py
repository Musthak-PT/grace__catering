from django.urls import include, path, re_path
from . import views
from django.contrib.auth.decorators import login_required
from rest_framework import routers

urlpatterns = [       
   re_path(r'^web/', include([
       
        path('subscription-mail', views.SubscriptionMailApiView.as_view()),
        
   ])),
]