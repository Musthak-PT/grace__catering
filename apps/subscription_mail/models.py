from django.db import models
from apps.authentication.models import AbstractDateFieldMix

# Create your models here.
class SubscribersList(AbstractDateFieldMix):
        subscribers_email=models.EmailField(null=True,blank=True)

        def __str__(self):
            return str(self.pk)
    
        class Meta:
            verbose_name            = "SubscribersList"
            verbose_name_plural     = "SubscribersList"