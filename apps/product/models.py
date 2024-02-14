from django.db import models
from solo_core.models import AbstractDateTimeFieldBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from random import randint
from uuid import uuid4
from apps.category.models import Category
# Create your models here.

class Product(AbstractDateTimeFieldBaseModel):
    slug            = models.SlugField(_('Slug'), max_length=100, editable=False, null=True, blank=True)
    product_name    = models.CharField(max_length=256)
    category        = models.ForeignKey(Category, blank=True, related_name="category", on_delete=models.CASCADE, null=True)
    class Meta: 
        verbose_name          = "Product"
        verbose_name_plural   = "Product"
        
    def save(self, *args, **kwargs):
        if not self.slug or self.id:
            self.slug = slugify(str(self.product_name))
            if Product.objects.filter(slug=self.product_name).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.product_name)) + '-' + str(randint(1, 9999999))
        super(Product, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.product_name