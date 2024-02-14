from django.urls import path, re_path, include
from . import views

urlpatterns = [       
   re_path(r'^web/', include([
      path('get-all-web-about-us', views.GetAllAboutUsWebAPIView.as_view()),
   ])),
]