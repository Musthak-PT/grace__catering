from django.urls import path,re_path,include
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'customer_management'


urlpatterns = [
    re_path(r'^customer-management/', include([
        path('', login_required(views.CustomerManagementView.as_view()), name='customer_management.view.index'),
        path('load_customer_management_datatable', login_required(views.LoadCustomerManagementDatatable.as_view()), name='load.customer_management.datatable'),
        path('download_customer_data/', login_required(views.DownloadCustomerDataView.as_view()), name='download_customer_data'),
        # path('<str:id>/detail-view/', login_required(views.ContactUsEnquieryDetailViewView.as_view()), name='contact-us-enquiry.detail-view'),
        # path('destroy_records/', login_required(views.DestroyContactUsEnquieryRecordsView.as_view()), name='contact-us-enquiry.records.destroy'),
        path('active/', login_required(views.CustomerManagementStatusChange.as_view()), name="active.or.inactive.customer_management"),
        path('customer/generate_excel', views.generate_excel, name='generate_excel'),
    ])),
     re_path(r'^promotion/', include([
        path('', login_required(views.CustomerPromotionView.as_view()), name='customer_promotion.index'),
        path('create/', login_required(views.CustomerPromotionCreateOrUpdateView.as_view()), name='customer_promotion.create'),
        path('<str:id>/update/', views.CustomerPromotionCreateOrUpdateView.as_view(), name='customer_promotion.update'),
        path('promotion-datatable', login_required(views.LoadCustomerPromotionDatatable.as_view()), name='load.customer_promotion.datatable'),
        path('destroy_records/', login_required(views.DestroyCustomerPromotionRecordsView.as_view()), name='customer_promotion.records.destroy'),
    ])),
     re_path(r'^room-booked-customer-management/', include([
        path('', login_required(views.RoomBookedCustomerManagementView.as_view()), name='room_booked_customers.view.index'),
        path('load_room_booked_customers_datatable', login_required(views.LoadRoomBookedCustomerManagementDatatable.as_view()), name='load.room_booked_customers.datatable'),
        path('download_customer_data/', login_required(views.DownloadCustomerDataView.as_view()), name='download_customer_data'),
        # path('<str:id>/detail-view/', login_required(views.ContactUsEnquieryDetailViewView.as_view()), name='contact-us-enquiry.detail-view'),
        # path('destroy_records/', login_required(views.DestroyContactUsEnquieryRecordsView.as_view()), name='contact-us-enquiry.records.destroy'),
        path('active/', login_required(views.CustomerManagementStatusChange.as_view()), name="active.or.inactive.customer_management"),
        path('customer/generate_room_booked_excel', views.generate_room_booked_excel, name='generate_room_booked_excel'),
    ])),
]