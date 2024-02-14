from django.urls import path, re_path, include
from . import views

urlpatterns = [       
   re_path(r'^web/', include([
      path('create-all-web-testimonial', views.TestimonialCreateApiView.as_view()),
      path('get-all-web-testimonial', views.GetAllTestimonialWebAPIView.as_view()),
   ])),
]