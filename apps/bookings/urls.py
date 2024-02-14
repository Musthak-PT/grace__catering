from django.urls import re_path, path, include
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'bookings'

urlpatterns = [
   re_path(r'^room-booking/', include([
        path('', login_required(views.ManualRoomBookingView.as_view()), name='manual_booking.index'),
        path('create/', login_required(views.ManualRoomBookingCreateOrUpdateView.as_view()), name='manual_booking.create'),
        path('<str:id>/update/', views.ManualRoomBookingCreateOrUpdateView.as_view(), name='manual_booking.update'),
        path('room-booking-datatable', login_required(views.LoadRoomBookingDatatable.as_view()), name='load.manual_booking.datatable'),
        path('payment-status-change/', login_required(views.RoomBookingPaymentStatusChange.as_view()), name="room_booking.payment_status_change"),
        path('get-booked-customer-images', views.GetBookingCustomerImages.as_view(), name='get.bookings_customer.images'),
    ])),
    re_path(r'^enquiry-booking/', include([
        path('', login_required(views.EnquiryListBookingView.as_view()), name='enquiry_list_booking.index'),
        path('enquiry-booking-datatable', login_required(views.LoadShowEnquiryBookingDatatable.as_view()), name='load.list_enquiry_booking.datatable'),
    ])),
]