from django.urls import path, re_path, include
from . import views

urlpatterns = [       
   re_path(r'^web/', include([
      path('get-all-AccommodationType', views.GetAllAccommodationTypeWebAPIView.as_view()),
      path('get-all-PropertyCollection', views.GetAllPropertyCollectionWebAPIView.as_view()),
      path('get-all-PropertyFacility', views.GetAllPropertyFacilityWebAPIView.as_view()),
      path('property-filtering-and-sorting', views.GetPropertyFilteringWebAPIView.as_view()),

      #Drop down listing
      path('get-dropdown-collection', views.GetCollectionDropdownApiView.as_view()),
      path('get-dropdown-accomadation-type', views.GetAccomadationTypeDropdownApiView.as_view()),
      path('get-dropdown-property-facility', views.GetPropertyFacilityDropdownApiView.as_view()),
      path('get-dropdown-room-types', views.GetPropertyRoomTypesDropdownApiView.as_view()),
      
      #Property detailed view
      path('get-property-detailed-view', views.GetPropertyDetailedApiView.as_view()),
      path('room-selection-filter', views.GetRoomSelectionApiView.as_view()),
      
      #room booking api
      path('hotel-room-booking', views.CreateRoomBookingApiView.as_view()),
      path('get-hotel-room-booking-profile-details', views.GetRoomBookingProfileApiView.as_view()),
      #room selcting from detailed view of property
      # path('choose-your-room-for-booking', views.GetChoosingRoomsApiView.as_view()),

      # My booking api
      path('my-booking-room-listing', views.GetMyBookingPropertiesApiView.as_view()),
      path('my-booking-room-detialed-view', views.GetMyBookingPropertiesDetailedApiView.as_view()),
      # Room booking api
      path('create-and-listing-room-booking', views.CreateAndListRoomBookingApiView.as_view()),
   ])),
]
