from django.db import models
from django.utils.translation import gettext_lazy as _
from uuid import uuid4
from apps.authentication.models import AbstractDateFieldMix
from apps.bookings.models import RoomBookedCustomerDetails
from apps.users.models import Users
from apps.property_management.models import PropertyManagement

def default_image():
    return f"default/image/default-image.png" 


# Create your models here.

def customer_image_media(self, filename):
    extension = filename.split('.')[-1].lower()
    upload_path = 'assets/customer-image/'
    return '{}{}.{}'.format(upload_path, uuid4(), extension)


class CustomerReview(AbstractDateFieldMix):
    RATINGS = [
    ('1', 'Very Bad'),
    ('2', 'Bad'),
    ('3', 'Good'),
    ('4','Very Good'),
    ('5','Excellent')
    ]
    user            = models.ForeignKey(RoomBookedCustomerDetails, on_delete=models.SET_NULL, null=True, blank=True)
    property        = models.ForeignKey(PropertyManagement, on_delete=models.SET_NULL, null=True, blank=True)
    rating          = models.CharField(_("Rating"),choices=RATINGS, max_length=250,null=True,blank=True)
    description     = models.CharField(_('Description'),max_length=200,null=True, blank=True,db_index=True)
    title           = models.TextField(_('Review'),null=True, blank=True,db_index=True)
    
    def __str__(self):
        return str(self.pk)
    
    class Meta:
        verbose_name = "CustomerReview"
        verbose_name_plural = "CustomerReview"