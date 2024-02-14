from django.urls import re_path,path, include
from . import views

urlpatterns = [
    re_path(r'^enquiry/', include([
        path('be-a-partner-form-submission', views.BeAPartnerEnquiryFromSubmissionApiView.as_view()),
        path('contact-us-form-submission', views.ContactUsEnquiryFromSubmissionApiView.as_view()),
        path('get-all-partners-logo-images', views.GetAllPartnerLogoImagesWebAPIView.as_view()),
    ]))
]