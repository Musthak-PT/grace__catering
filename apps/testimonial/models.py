from django.db import models
from solo_core.models import AbstractDateTimeFieldBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from random import randint

# Create your models here.
def testimonial_image(self, filename):
    return f"assets/users/{filename}"

def testimonial_default_image(): 
    return f"default/default-image/default-image-for-no-image.png"

class Testimonial(AbstractDateTimeFieldBaseModel):
    slug                    = models.SlugField(_('Slug'), max_length=100, editable=False)
    testimonial_title       = models.CharField(max_length=256,null=True, blank=True)
    testimonial_image       = models.FileField(_('Image'), null=True, blank=True, upload_to=testimonial_image, default=testimonial_default_image)
    testimonial_fullname    = models.CharField(max_length=256,null=True,blank=True)
    testimonial_description = models.TextField(null=True,blank=True)
    
    class Meta:
        verbose_name          = "Testimonial"
        verbose_name_plural   = "Testimonial"
        
    def save(self, *args, **kwargs):
        if not self.slug or self.testimonial_title:
            self.slug = slugify(str(self.testimonial_title))
            if Testimonial.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.testimonial_title)) + '-' + str(randint(1, 9999999))
        super(Testimonial, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.testimonial_title