from celery import shared_task
from datetime import datetime
import logging
from apps.customers.promotion_email import auto_review_mail_send
from django.db.models import Q
from apps.bookings.models import HotelRoomBookingBookingPrice
from apps.property_management.models import PropertyCollection
from apps.review.middleware import get_current_request
logger = logging.getLogger(__name__)

@shared_task
def auto_review_email():
    last_object = PropertyCollection.objects.filter(id=1).first()
    test = HotelRoomBookingBookingPrice.objects.all()
    price_booking_obj = HotelRoomBookingBookingPrice.objects.filter(Q(booked_room__check_out__date=datetime.now().date()))
    auto_review_mail_send(price_booking_obj)