"""root_project_django_v4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.static import serve
from solo_core.views import page_not_found_view, custom_500

admin.site.site_header = "Solo"
admin.site.site_title = "Solo"

schema_view = get_schema_view(
   openapi.Info(
      title="SOLO",
      default_version='v1',
      terms_of_service="",
      contact=openapi.Contact(email="yadu@aventusinformatics.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^assets/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),


    path('', include('apps.home.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('auth/', include('apps.authentication.urls')),
    path('contact-us/', include('apps.contactus.urls')),
    path('offer/', include('apps.offer.urls')),
    path('about-us/', include('apps.aboutus.urls')),
    path('wishlist/', include('apps.wishlist.urls')),
    path('subscription_mail/', include('apps.subscription_mail.urls')),
    path('banner-image/', include('apps.bannerimage.urls')),
    path('question-and-answers/', include('apps.questionandanswers.urls')),
    path('our-team/', include('apps.ourteam.urls')),
    path('testimonial/', include('apps.testimonial.urls')),
    path('review/', include('apps.review.urls')),
    path('admins/', include('apps.admins.urls')),
    path('ad_management/', include('apps.ad_management.urls')),
    path('property-management/', include('apps.property_management.urls')),
    path('customer-management/', include('apps.customers.urls')),
    path('booking-management/', include('apps.bookings.urls')),
    path('category/', include('apps.category.urls')),
    path('product/', include('apps.product.urls')),
    path('user-management/', include('apps.user_management.urls')),
    
    
    
    re_path(r'^api/', include([
        
        path('auth/', include('apps.authentication.api.urls')),
        path('users/', include('apps.users.api.urls')),
        path('home/', include('apps.home.api.urls')),
        path('contact-us/', include('apps.contactus.api.urls')),
        path('testimonial/', include('apps.testimonial.api.urls')),
        path('about-us/', include('apps.aboutus.api.urls')),
        path('subscription_mail/', include('apps.subscription_mail.api.urls')),
        path('offer/', include('apps.offer.api.urls')),
        path('wishlist/', include('apps.wishlist.api.urls')),
        path('banner-image/', include('apps.bannerimage.api.urls')),
        path('question-and-answers/', include('apps.questionandanswers.api.urls')),
        path('our-team/', include('apps.ourteam.api.urls')),
        path('property-management/', include('apps.property_management.api.urls')),
        path('review/', include('apps.review.api.urls')),
        path('ad_management/', include('apps.ad_management.api.urls')),
        path('booking_management/', include('apps.bookings.api.urls')),
        path('customer-management/', include('apps.customers.api.urls')),

    
        re_path(r'^docs/', include([

            path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
            path("redoc", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

        ])),    
    ])),    
    
        
    
] 


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = page_not_found_view
handler500 = custom_500
