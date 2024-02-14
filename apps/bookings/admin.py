from django.contrib import admin
from .models import *


# Register your models here.

admin.site.register(RoomBookedCustomerDetails)
admin.site.register(HotelRoomBookingCustomerDetails)
admin.site.register(HotelRoomBooking)
admin.site.register(BookingPrice)
admin.site.register(HotelRoomBookingBookingPrice)