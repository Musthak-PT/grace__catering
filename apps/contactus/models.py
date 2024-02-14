from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.authentication.models import AbstractDateFieldMix

# Create your models here.
class ContactUs(AbstractDateFieldMix):
    ENQUIRY_TYPE = [
        ('1', 'Customer'),
        ('2', 'Partner'),
    ]
    name            = models.CharField(max_length=250,blank=True,null=True,db_index=True)
    enquiry_type    = models.CharField(max_length=100,choices=ENQUIRY_TYPE, blank=True, null=True)
    message         = models.TextField(verbose_name="Message", blank=True, null=True, help_text="Enter your text here.", db_index=True)
    email           = models.EmailField(blank=True,null=True,db_index=True)
    mobile_number   = models.CharField(max_length=50,blank=True,null=True,db_index=True)
    state           = models.CharField(max_length=50,blank=True,null=True,db_index=True)
    is_contacted    = models.BooleanField(default=False)
    full_name       = models.CharField(max_length=50,blank=True,null=True,db_index=True)
    
    def __str__(self):
        return str(self.pk)
    
    class Meta:
        verbose_name            = "Contact_us"
        verbose_name_plural     = "Contact_us"


def partner_logo_image(self, filename):
    return f"assets/partner-logo-image/{filename}"


def partner_default_image(): 
    return f"default/default-image/default-image-for-no-image.png"

class PartnersLogo(AbstractDateFieldMix):
        partner_logo_image   = models.FileField(_('Partner Logo Image'), null=True, blank=True, upload_to=partner_logo_image, default=partner_default_image)

        def __str__(self):
            return str(self.pk)
    
        class Meta:
            verbose_name            = "Partners"
            verbose_name_plural     = "Partners"

    
