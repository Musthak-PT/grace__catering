from django.db import models
from solo_core.models import AbstractDateTimeFieldBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from random import randint
from uuid import uuid4
# Create your models here.
def banner_image(self, filename):
    return f"assets/banner-image/{filename}"


def banner_default_image(): 
    return f"default/default-image/default-image-for-no-image.png"

class BannerImagesDetail(AbstractDateTimeFieldBaseModel):
    slug                      = models.SlugField(_('Slug'), max_length=100, editable=False, null=True, blank=True)
    title                     = models.CharField(max_length=100,null=True, blank=True)
    class Meta: 
        verbose_name          = "BannerImagesDetail"
        verbose_name_plural   = "BannerImagesDetails"
        
    def save(self, *args, **kwargs):
        if not self.slug or self.id:
            self.slug = slugify(str(self.id))
            if BannerImagesDetail.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.id)) + '-' + str(randint(1, 9999999))
        super(BannerImagesDetail, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.id

class BannerImages(AbstractDateTimeFieldBaseModel):
    slug                      = models.SlugField(_('Slug'), max_length=100, editable=False, null=True, blank=True)
    banner_details            = models.ForeignKey(BannerImagesDetail, related_name="banner_image_details", on_delete=models.CASCADE, blank=True, null=True)
    image                     = models.FileField(_('Banner Image'), null=True, blank=True, upload_to=banner_image, default=banner_default_image)
    uuid                      = models.CharField(_('Banner Image UUID'),  max_length=150, editable=False, null=True, blank=True)
    
    class Meta: 
        verbose_name          = "BannerImage"
        verbose_name_plural   = "BannerImages"
        
    
    
    def save(self, *args, **kwargs):
        if not self.slug or self.id:
            self.slug = slugify(str(self.id))
            if BannerImages.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.id)) + '-' + str(randint(1, 9999999))
        super(BannerImages, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.id
    
    
def banner_temporary_image_upload_image_dir(request):
    return 'assets/banner_image/image/{}/{}.png'.format(request.user.id, uuid4())