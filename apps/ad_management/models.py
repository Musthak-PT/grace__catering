from django.db import models
from solo_core.models import AbstractDateTimeFieldBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from random import randint
from apps.property_management.models import PropertyManagement
# Create your models here.
def ad_image(self, filename):
    return f"assets/ad_management/{filename}"


def ad_default_image(): 
    return f"default/default-image/default-image-for-no-image.png"

class AdManagement(AbstractDateTimeFieldBaseModel):
    slug              = models.SlugField(_('Slug'), max_length=100, editable=False, null=True, blank=True)
    ad_title          = models.CharField(max_length=256,null=True, blank=True)
    ad_description    = models.TextField(null=True,blank=True)
    image             = models.FileField(_('Banner Image'), null=True, blank=True, upload_to=ad_image, default=ad_default_image)
    property          = models.ForeignKey(PropertyManagement, blank=True, related_name="ad_management_property", on_delete=models.CASCADE, null=True)
    
    class Meta: 
        verbose_name          = "AdManagement"
        verbose_name_plural   = "AdManagement"
        
    def save(self, *args, **kwargs):
        if not self.slug or self.ad_title:
            self.slug = slugify(str(self.ad_title))
            if AdManagement.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.ad_title)) + '-' + str(randint(1, 9999999))
        super(AdManagement, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.ad_title