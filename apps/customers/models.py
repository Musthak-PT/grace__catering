from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.authentication.models import AbstractDateFieldMix
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from random import randint

from apps.users.models import Users

# Create your models here.

def promotion_image(self, filename):
    return f"assets/promotion/{filename}"


def promotion_default_image(): 
    return f"default/default-image/default-image-for-no-image.png"


class Promotions(AbstractDateFieldMix):
    slug            = models.SlugField(_('Slug'), max_length=100, editable=False)
    title           = models.CharField(max_length=50,blank=True,null=True,db_index=True)
    subject         = models.CharField(max_length=100,blank=True,null=True,db_index=True)
    message         = models.TextField(verbose_name="Message", blank=True, null=True, help_text="Enter your text here.", db_index=True)
    image           = models.FileField(_('Banner Image'), null=True, blank=True, upload_to=promotion_image, default=promotion_default_image)

    class Meta:
        verbose_name          = "Promotion"
        verbose_name_plural   = "Promotions"
        
    # slug for Medications table with releated to name
    def save(self, *args, **kwargs):
        if not self.slug or self.title:
            self.slug = slugify(str(self.title))
            if Promotions.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.title)) + '-' + str(randint(1, 9999999))
        super(Promotions, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
class PromotionCustomer(AbstractDateFieldMix):
    
    TABLE_TYPES = [
        ('1', 'User'),
        ('2', 'Booking'),
    ]
        
    slug                 = models.SlugField(_('Slug'), max_length=100, editable=False)
    table_type           = models.CharField(max_length=100,choices=TABLE_TYPES, blank=True, null=True)
    promotion            = models.ForeignKey(Promotions, blank=True, related_name="promotion_title", on_delete=models.SET_NULL, null=True)
    email                = models.EmailField(_('Email'), max_length = 255, blank = True, null = True)
    full_name            = models.CharField(_('Full Name'), max_length = 200, blank = True, null = True)
    
    class Meta:
        verbose_name          = "PromotionCustomer"
        verbose_name_plural   = "PromotionCustomers"
        
    # slug for Medications table with releated to name
    def save(self, *args, **kwargs):
        if not self.slug or self.full_name:
            self.slug = slugify(str(self.full_name))
            if PromotionCustomer.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.full_name)) + '-' + str(randint(1, 9999999))
        super(PromotionCustomer, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.full_name