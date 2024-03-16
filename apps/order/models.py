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
    customer_details = models.CharField(max_length=90, null=True, blank=True)
    order_date = models.DateTimeField(null=True, blank=True)
    products = models.ManyToManyField(Product, through='OrderItem')
    
class OrderItem(AbstractDateTimeFieldBaseModel):
    order = models.ForeignKey(OrderProduct, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.product} - Quantity: {self.quantity}, Price: {self.price}"