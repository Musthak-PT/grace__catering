from django.db import models
from solo_core.models import AbstractDateTimeFieldBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from random import randint

# Create your models here.
class AboutUs(AbstractDateTimeFieldBaseModel):
    slug                 = models.SlugField(_('Slug'), max_length=100, editable=False)
    title                = models.CharField(max_length=256, blank=True)
    description          = models.TextField(null=True,blank=True)
    
    class Meta:
        verbose_name = "AboutUs" 
        verbose_name_plural = "AboutUs"
        
    def save(self, *args, **kwargs):
        if not self.slug or self.description:
            self.slug = slugify(str(self.description))
            if AboutUs.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.description)) + '-' + str(randint(1, 9999999))
        super(AboutUs, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.description