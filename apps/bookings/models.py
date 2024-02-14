from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from random import randint
from apps.property_management.models import HotelRoom
from solo_core.models import AbstractDateTimeFieldBaseModel
from apps.users.models import Users

# Create your models here.

def guest_document_file(self, filename):
    return f"assets/guest-document/{filename}"


def banner_default_image(): 
    return f"default/default-image/default-image-for-no-image.png"


class RoomBookedCustomerDetails(AbstractDateTimeFieldBaseModel):
    slug                = models.SlugField(_('Slug'), max_length=100, editable=False,null=True, blank=True)
    full_name           = models.CharField(max_length=100,null=True, blank=True)
    email_address       = models.CharField(max_length=100,null=True, blank=True)
    mobile_number       = models.CharField(max_length=100,null=True, blank=True)
    # user_details        = models.ForeignKey(Users, related_name="guest_user_details", on_delete=models.SET_NULL, blank=True, null=True)
    dob                 = models.DateTimeField(null=True, blank=True)
    guest_address       = models.CharField(max_length=256,null=True, blank=True)
    total_booked_price  = models.CharField(max_length=100,null=True, blank=True)
    is_enquired         = models.BooleanField(default=False)
    document            = models.FileField(_('Guest Document'), null=True, blank=True, upload_to=guest_document_file, default=banner_default_image)
    
    class Meta:
        verbose_name          = "RoomBookedCustomerDetails"
        verbose_name_plural   = "RoomBookedCustomerDetails"
        
    def save(self, *args, **kwargs):
        if not self.slug or self.full_name:
            self.slug = slugify(str(self.full_name))
            if RoomBookedCustomerDetails.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.full_name)) + '-' + str(randint(1, 9999999))
        super(RoomBookedCustomerDetails, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.full_name

#     slug             = models.SlugField(_('Slug'), max_length=100, editable=False,null=True, blank=True)
#     room_id          = models.ForeignKey(HotelRoom, related_name="hotel_temp_room_booking", on_delete=models.SET_NULL, blank=True, null=True)
#     quantity         = models.IntegerField(null=True,blank=True)
#     check_in         = models.DateTimeField(null=True, blank=True)
#     check_out        = models.DateTimeField(null=True, blank=True)
#     customer_details = models.ForeignKey(RoomBookedCustomerDetails, related_name="booked_temp_customer_details", on_delete=models.SET_NULL, blank=True, null=True)
    
#     class Meta:
#         verbose_name          = "HotelRoomTempBooking"
#         verbose_name_plural   = "HotelRoomTempBookings"
        
#     def save(self, *args, **kwargs):
#         if not self.slug or self.room_id:
#             self.slug = slugify(str(self.room_id))
#             if HotelRoomTempBooking.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
#                 self.slug = slugify(str(self.room_id)) + '-' + str(randint(1, 9999999))
#         super(HotelRoomTempBooking, self).save(*args, **kwargs)

#     def __str__(self):
#         return str(self.id)
    
class HotelRoomBooking(AbstractDateTimeFieldBaseModel):
    slug             = models.SlugField(_('Slug'), max_length=100, editable=False,null=True, blank=True)
    room_sl_no       = models.CharField(max_length=100,null=True, blank=True)
    room_id          = models.ForeignKey(HotelRoom, related_name="hotel_room_booking", on_delete=models.SET_NULL, blank=True, null=True)
    quantity         = models.IntegerField(null=True,blank=True)
    check_in         = models.DateTimeField(null=True, blank=True)
    check_out        = models.DateTimeField(null=True, blank=True)
    adults           = models.IntegerField(null=True,blank=True)
    childrens        = models.IntegerField(null=True,blank=True)
    booked_room_price = models.CharField(max_length=100,null=True, blank=True)

    class Meta:
        verbose_name          = "HotelRoomBooking"
        verbose_name_plural   = "HotelRoomBookings"
        
    def save(self, *args, **kwargs):
        if not self.slug or self.room_id:
            self.slug = slugify(str(self.room_id))
            if HotelRoomBooking.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.room_id)) + '-' + str(randint(1, 9999999))
        super(HotelRoomBooking, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)
    

class HotelRoomBookingCustomerDetails(AbstractDateTimeFieldBaseModel):
    slug                     = models.SlugField(_('Slug'), max_length=100, editable=False, null=True, blank=True)
    guest_details            = models.ForeignKey(RoomBookedCustomerDetails, related_name="hotel_room_booked_customer_details", on_delete=models.CASCADE, blank=True, null=True)
    booked_room              = models.ForeignKey(HotelRoomBooking, related_name="booked_room_customer_details", on_delete=models.CASCADE, blank=True, null=True)
    
    
    class Meta: 
        verbose_name          = "HotelRoomBookingCustomerDetails"
        verbose_name_plural   = "HotelRoomBookingCustomerDetails"
        
    
    def save(self, *args, **kwargs):
        if not self.slug or self.id:
            self.slug = slugify(str(self.id))
            if HotelRoomBookingCustomerDetails.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.id)) + '-' + str(randint(1, 9999999))
        super(HotelRoomBookingCustomerDetails, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.id)
    
    
class BookingPrice(AbstractDateTimeFieldBaseModel):
    slug                     = models.SlugField(_('Slug'), max_length=100, editable=False, null=True, blank=True)
    total_booked_price       = models.CharField(max_length=100,null=True, blank=True)
    is_paid                  = models.BooleanField(default=False)
    is_enquiry               = models.BooleanField(default=False)
    customer_details         = models.ForeignKey(RoomBookedCustomerDetails, related_name="booked_customer_price_details", on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta: 
        verbose_name          = "BookingPrice"
        verbose_name_plural   = "BookingPrices"
        
    
    def save(self, *args, **kwargs):
        if not self.slug or self.id:
            self.slug = slugify(str(self.id))
            if BookingPrice.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.id)) + '-' + str(randint(1, 9999999))
        super(BookingPrice, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.id)
    
    
class HotelRoomBookingBookingPrice(AbstractDateTimeFieldBaseModel):
    slug                     = models.SlugField(_('Slug'), max_length=100, editable=False, null=True, blank=True)
    booked_room              = models.ForeignKey(HotelRoomBooking, related_name="hotel_room_booked_guest_details", on_delete=models.CASCADE, blank=True, null=True)
    booked_price             = models.ForeignKey(BookingPrice, related_name="booked_room_details", on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta: 
        verbose_name          = "HotelRoomBookingBookingPrice"
        verbose_name_plural   = "HotelRoomBookingBookingPrices"
        
    
    def save(self, *args, **kwargs):
        if not self.slug or self.id:
            self.slug = slugify(str(self.id))
            if HotelRoomBookingBookingPrice.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.id)) + '-' + str(randint(1, 9999999))
        super(HotelRoomBookingBookingPrice, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.id)