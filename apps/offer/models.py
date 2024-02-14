from django.db import models
from apps.authentication.models import AbstractDateFieldMix
from django.utils.text import slugify
from random import randint
from django.utils.translation import gettext_lazy as _
# Create your models here.

def offer_image(self, filename):
    return f"assets/offer/{filename}"


def offer_default_image(): 
    return f"default/default-image/default-image-for-no-image.png"

class PropertyOffer(AbstractDateFieldMix):
    slug                = models.SlugField(_('Slug'), max_length=100, editable=False)
    room_property       = models.ForeignKey('property_management.PropertyManagementHotelRoom', on_delete=models.CASCADE, related_name='%(class)s_created', null=True, blank=True)#Used for taking the room which has offer 
    start_date          = models.DateField(null=True, blank=True)
    end_date            = models.DateField(null=True, blank=True)
    offer_percentage    = models.CharField(max_length=256, null=True, blank=True)
    title               = models.CharField(max_length=256, null=True, blank=True)
    description         = models.TextField(null=True,blank=True)
    
    image               = models.FileField(_('Offer Image Image'), null=True, blank=True, upload_to=offer_image, default=offer_default_image)
    
    class Meta:
        verbose_name = "PropertyOffer" 
        verbose_name_plural = "PropertyOffer"
        
    def save(self, *args, **kwargs):
        if not self.slug or self.offer_percentage:
            self.slug = slugify(str(self.offer_percentage))
            if PropertyOffer.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.offer_percentage)) + '-' + str(randint(1, 9999999))
        super(PropertyOffer, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.offer_percentage