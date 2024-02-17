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
    customer_details    = models.ForeignKey(Users, blank=True, related_name="users", on_delete=models.CASCADE, null=True)
    order_date          = models.DateField(null=True, blank=True)
    order_time          = models.TimeField(null=True, blank=True)
    quantity            = models.ImageField(null=True, blank=True)
    class Meta                : 
        verbose_name          = "Order Product"
        verbose_name_plural   = "Order Product"
        
    def save(self, *args, **kwargs):
        if not self.slug or self.id:
            self.slug = slugify(str(self.quantity))
            if OrderProduct.objects.filter(slug=self.quantity).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.quantity)) + '-' + str(randint(1, 9999999))
        super(OrderProduct, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.id
