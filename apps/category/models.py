from django.db import models
from solo_core.models import AbstractDateTimeFieldBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from random import randint
from uuid import uuid4
# Create your models here.

class Category(AbstractDateTimeFieldBaseModel):
    slug           = models.SlugField(_('Slug'), max_length=100, editable=False, null=True, blank=True)
    category_name  = models.CharField(max_length=256)
    class Meta: 
        verbose_name          = "Category"
        verbose_name_plural   = "Category"
        
    def save(self, *args, **kwargs):
        if not self.slug or self.id:
            self.slug = slugify(str(self.category_name))
            if Category.objects.filter(slug=self.category_name).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.category_name)) + '-' + str(randint(1, 9999999))
        super(Category, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.category_name