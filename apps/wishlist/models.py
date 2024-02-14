from django.db import models
from solo_core.models import AbstractDateTimeFieldBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from random import randint
from apps.users.models import Users
from apps.property_management.models import PropertyManagement

# Create your models here.
class WishList(AbstractDateTimeFieldBaseModel):
    user        = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    property    = models.ForeignKey(PropertyManagement, on_delete=models.CASCADE, null=True,blank=True)
    
    class Meta:
        verbose_name          = "WishList"
        verbose_name_plural   = "WishLists"
                
    def __str__(self):
        return str(self.user.full_name)
