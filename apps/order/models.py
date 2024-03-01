from django.db import models
from solo_core.models import AbstractDateTimeFieldBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from random import randint
from apps.product.models import Product
from uuid import uuid4
from apps.users.models import Users
# Create your models here.

class OrderProduct(AbstractDateTimeFieldBaseModel):
    slug                = models.SlugField(_('Slug'), max_length=100, editable=False, null=True, blank=True)
    product_name        = models.ForeignKey(Product, blank=True, related_name="product", on_delete=models.CASCADE, null=True)
    customer_details    = models.CharField(max_length=90,null=True, blank=True)
    order_date          = models.DateTimeField(null=True, blank=True)
    
    quantity            = models.CharField(max_length=90,null=True, blank=True)
    
    price       = models.CharField(max_length=90,null=True, blank=True)
    Total=models.IntegerField(null=True)
    class Meta                : 
        verbose_name          = "Order Product"
        verbose_name_plural   = "Order Product"
        
    