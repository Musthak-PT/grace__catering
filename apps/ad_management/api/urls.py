from django.urls import path, re_path, include
from . import views

urlpatterns = [       
   re_path(r'^web/', include([
       
      path('get-all-ad-images', views.GetAdImagesWebAPIView.as_view()),
      
   ])),
]