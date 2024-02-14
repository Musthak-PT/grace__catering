from django.urls import path, re_path,include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'property_management'

urlpatterns = [
    re_path(r'^accommodation-type/', include([
        path('', login_required(views.AccommodationTypeView.as_view()), name='accommodation_type.index'),
        path('create/', login_required(views.AccommodationTypeCreateOrUpdateView.as_view()), name='accommodation_type.create'),
        path('<str:id>/update/', views.AccommodationTypeCreateOrUpdateView.as_view(), name='accommodation_type.update'),
        path('accommodation-type-datatable', login_required(views.LoadAccommodationTypeDatatable.as_view()), name='load.accommodation_type.datatable'),
        path('destroy_records/', login_required(views.DestroyAccommodationTypeRecordsView.as_view()), name='accommodation_type.records.destroy'),
        # path('active-or-inactive/', login_required(views.AccommodationTypeStatusChange.as_view()), name="accommodation_type.status_change"),
    ])),
    re_path(r'^property-collections/', include([
        path('', login_required(views.PropertyCollectionView.as_view()), name='property_collection.index'),
        path('create/', login_required(views.PropertyCollectionCreateOrUpdateView.as_view()), name='property_collection.create'),
        path('<str:id>/update/', views.PropertyCollectionCreateOrUpdateView.as_view(), name='property_collection.update'),
        path('property-collections-datatable', login_required(views.LoadPropertyCollectionDatatable.as_view()), name='load.property_collection.datatable'),
        path('destroy_records/', login_required(views.DestroyPropertyCollectionRecordsView.as_view()), name='property_collection.records.destroy'),
        # path('active-or-inactive/', login_required(views.AccommodationTypeStatusChange.as_view()), name="accommodation_type.status_change"),
    ])),
    re_path(r'^property-facility/', include([
        path('', login_required(views.PropertyFacilityView.as_view()), name='property_facility.index'),
        path('create/', login_required(views.PropertyFacilityCreateOrUpdateView.as_view()), name='property_facility.create'),
        path('<str:id>/update/', views.PropertyFacilityCreateOrUpdateView.as_view(), name='property_facility.update'),
        path('property-facility-datatable', login_required(views.LoadPropertyFacilityDatatable.as_view()), name='load.property_facility.datatable'),
        path('destroy_records/', login_required(views.DestroyPropertyFacilityRecordsView.as_view()), name='property_facility.records.destroy'),
        # path('active-or-inactive/', login_required(views.AccommodationTypeStatusChange.as_view()), name="accommodation_type.status_change"),
    ])),
    re_path(r'^room-type/', include([
        path('', login_required(views.RoomTypeView.as_view()), name='room_type.index'),
        path('create/', login_required(views.RoomTypeCreateOrUpdateView.as_view()), name='room_type.create'),
        path('<str:id>/update/', views.RoomTypeCreateOrUpdateView.as_view(), name='room_type.update'),
        path('room-type-datatable', login_required(views.LoadRoomTypeDatatable.as_view()), name='load.room_type.datatable'),
        path('destroy_records/', login_required(views.DestroyRoomTypeRecordsView.as_view()), name='room_type.records.destroy'),
        path('active-or-inactive/', login_required(views.RoomTypeStatusChange.as_view()), name="room_type.status_change"),
    ])),
    re_path(r'^', include([
        path('', login_required(views.PropertyManagementView.as_view()), name='property_management.index'),
        path('create/', login_required(views.PropertyManagementCreateOrUpdateView.as_view()), name='property_management.create'),
        path('property-image-upload', login_required(views.PropertyImageUploadView.as_view()), name='property_management.image.upload'),
        path('destroy-temporary-image-upload', login_required(views.TemporaryImageDestroyView.as_view()), name='property_management.temporary.image.destroy'),
        path('<str:id>/update/', views.PropertyManagementCreateOrUpdateView.as_view(), name='property_management.update'),
        path('property-management-datatable', login_required(views.LoadPropertyManagementDatatable.as_view()), name='load.property_management.datatable'),
        path('get-property-management-images', views.GetPropertyManagementImages.as_view(), name='get.property_management.images'),
        path('destroy_records/', login_required(views.DestroyPropertyManagementRecordsView.as_view()), name='property_management.records.destroy'),
        path('active-or-inactive/', login_required(views.PropertyManagementStatusChange.as_view()), name="property_management.status_change"),


        path('room-image-upload', login_required(views.RoomImageUploadView.as_view()), name='room.image.upload'),
        path('destroy-temporary-room-image-upload', login_required(views.TemporaryRoomImageDestroyView.as_view()), name='room.temporary.image.destroy'),
        path('get-room-images', views.GetPropertyRoomImages.as_view(), name='get.room.images'),
        path('save-room-details', views.SavePropertyRoomDetails.as_view(), name='save.property.room'),
    ])),
]
