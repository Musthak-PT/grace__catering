from django.urls import path, re_path, include
from . import views

urlpatterns = [       
   re_path(r'^web/', include([
      path('create-wishlist', views.WishlistCreateApiView.as_view()),
      path('listing-wishlisted-properties', views.ListingWishlistApiView.as_view()),
   ])),
]