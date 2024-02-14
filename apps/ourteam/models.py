from django.db import models
from solo_core.models import AbstractDateTimeFieldBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from random import randint

# Create your models here.
def our_team_image(self, filename):
    return f"assets/our-team/{filename}"


def ourteam_default_image(): 
    return f"default/default-image/default-image-for-no-image.png"

class OurTeam(AbstractDateTimeFieldBaseModel):
    slug        = models.SlugField(_('Slug'), max_length=100, editable=False)
    fullname    = models.CharField(max_length=256, blank=True)
    designation = models.CharField(max_length=256, blank=True)
    image       = models.FileField(_('Facility Image'), null=True, blank=True, upload_to=our_team_image, default=ourteam_default_image)
    
    class Meta:
        verbose_name          = "OurTeam"
        verbose_name_plural   = "OurTeam"
        
    # slug for Medications table with releated to name
    def save(self, *args, **kwargs):
        if not self.slug or self.fullname:
            self.slug = slugify(str(self.fullname))
            if OurTeam.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.fullname)) + '-' + str(randint(1, 9999999))
        super(OurTeam, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.fullname