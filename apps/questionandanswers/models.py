from django.db import models
from solo_core.models import AbstractDateTimeFieldBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from random import randint

# Create your models here.
class QuestionAndAnswers(AbstractDateTimeFieldBaseModel):
    slug        = models.SlugField(_('Slug'), max_length=100, editable=False)
    question    = models.CharField(max_length=256, blank=True)
    answer      = models.TextField(null=True,blank=True)
    
    class Meta:
        verbose_name          = "QuestionAndAnswers"
        verbose_name_plural   = "QuestionAndAnswers"
        
    def save(self, *args, **kwargs):
        if not self.slug or self.question:
            self.slug = slugify(str(self.question))
            if QuestionAndAnswers.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.question)) + '-' + str(randint(1, 9999999))
        super(QuestionAndAnswers, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.question