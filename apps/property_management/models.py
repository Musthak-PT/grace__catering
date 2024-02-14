from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from random import randint
from solo_core.models import AbstractDateTimeFieldBaseModel
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from apps.users.validators import validate_possible_number
from uuid import uuid4
from apps.offer.models import PropertyOffer
from apps.users.models import Users


# Create your models here.

# Acccommodation Type started

class AccommodationType(AbstractDateTimeFieldBaseModel):
    slug                 = models.SlugField(_('Slug'), max_length=100, editable=False)
    name                 = models.CharField(max_length=256, blank=True)
    description          = models.TextField(null=True,blank=True)
    adults               = models.CharField(max_length=256, blank=True)
    
    class Meta:
        verbose_name = "AccommodationType" 
        verbose_name_plural = "AccommodationTypes"
        
    # slug for Medications table with releated to name
    def save(self, *args, **kwargs):
        if not self.slug or self.name:
            self.slug = slugify(str(self.name))
            if AccommodationType.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.name)) + '-' + str(randint(1, 9999999))
        super(AccommodationType, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
# End

# Property Collection start
class PropertyCollection(AbstractDateTimeFieldBaseModel):
    slug                 = models.SlugField(_('Slug'), max_length=100, editable=False)
    name                 = models.CharField(max_length=256, blank=True)
    description          = models.TextField(null=True,blank=True)
    
    class Meta:
        verbose_name = "PropertyCollection" 
        verbose_name_plural = "PropertyCollections"
        
    # slug for Medications table with releated to name
    def save(self, *args, **kwargs):
        if not self.slug or self.name:
            self.slug = slugify(str(self.name))
            if PropertyCollection.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.name)) + '-' + str(randint(1, 9999999))
        super(PropertyCollection, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.name

# End

# Property Facility 

def property_facility_image(self, filename):
    return f"assets/property_management/property_facility/{filename}"


def property_facility_default_image(): 
    return f"default/default-image/default-image-for-no-image.png"

class PropertyFacility(AbstractDateTimeFieldBaseModel):
    slug                 = models.SlugField(_('Slug'), max_length=100, editable=False)
    name                 = models.CharField(max_length=256, blank=True)
    description          = models.TextField(null=True,blank=True)
    # image                = models.FileField(_('Facility Image'), null=True, blank=True, upload_to=property_facility_image, default=property_facility_default_image)
    
    class Meta:
        verbose_name = "PropertyFacility" 
        verbose_name_plural = "PropertyFacilities"
        
    # slug for Medications table with releated to name
    def save(self, *args, **kwargs):
        if not self.slug or self.name:
            self.slug = slugify(str(self.name))
            if PropertyFacility.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.name)) + '-' + str(randint(1, 9999999))
        super(PropertyFacility, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.name

# End

# Room Type

class RoomType(AbstractDateTimeFieldBaseModel):
    slug                 = models.SlugField(_('Slug'), max_length=100, editable=False)
    name                 = models.CharField(max_length=256, blank=True)
    adults               = models.CharField(max_length=256, blank=True)
    description          = models.TextField(null=True,blank=True)
    
    class Meta:
        verbose_name          = "RoomType"
        verbose_name_plural   = "RoomTypes"
        
        
    # slug for Medications table with releated to name
    def save(self, *args, **kwargs):
        if not self.slug or self.name:
            self.slug = slugify(str(self.name))
            if RoomType.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.name)) + '-' + str(randint(1, 9999999))
        super(RoomType, self).save(*args, **kwargs)


    def __str__(self):
        return self.name
    
# End

# Property Management start

def property_management_image(self, filename):
    return f"assets/property_management/image/{filename}"


def property_management_default_image()             : 
    return f"default/default-image/default-image-for-no-image.png"

def property_room_image(self, filename):
    return f"assets/property_management/property_room/{filename}"

def property_room_default_image()             : 
    return f"default/default-image/default-image-for-no-image.png"


class PossiblePhoneNumberField(PhoneNumberField):
    """Less strict field for phone numbers written to database."""
    default_validators = [validate_possible_number]
    
class PropertyAddress(models.Model):
    street              = models.CharField(max_length=256, blank=True, null=True)
    city                = models.CharField(max_length=256, blank=True, null=True)
    city_area           = models.CharField(max_length=128, blank=True, null=True)
    postal_code         = models.CharField(max_length=20, blank=True, null=True)
    phone               = PossiblePhoneNumberField(blank=True, default="", null=True)
    alternative_phone   = PossiblePhoneNumberField(blank=True, default="", null=True)
    
    class Meta:
        ordering = ("pk",)

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)


    def __eq__(self, other):
        if not isinstance(other, PropertyAddress):
            return False
        return self.as_data() == other.as_data()

    __hash__ = models.Model.__hash__
    

class PropertyManagement(AbstractDateTimeFieldBaseModel):
    slug                 = models.SlugField(_('Slug'), max_length=100, editable=False)
    name                 = models.CharField(max_length=256, blank=True, null=True)
    description          = models.TextField(null=True,blank=True)
    address              = models.ForeignKey(PropertyAddress, blank=True, related_name="property_address", on_delete=models.SET_NULL, null=True)
    accomodation_type    = models.ForeignKey(AccommodationType, blank=True, related_name="accomodation_type", on_delete=models.SET_NULL, null=True)
    # room               = models.ManyToManyField(HotelRoom, related_name="+")
    latitude             = models.CharField(max_length=256, blank=True, null=True)
    longitude            = models.CharField(max_length=256, blank=True, null=True)
    location             = models.CharField(max_length=256, blank=True, null=True)
    no_of_rooms          = models.CharField(max_length=256, blank=True, null=True)
    location_distance    = models.CharField(max_length=256, blank=True, null=True) #Used for show the km from any preferred places
    assigned_to          = models.ForeignKey(Users, blank=True, related_name="assigned_to", on_delete=models.SET_NULL, null=True,)
    
    class Meta:
        verbose_name = "PropertyManagement"
        verbose_name_plural = "PropertyManagements"
        
        
    # slug for Medications table with releated to name
    def save(self, *args, **kwargs):
        if not self.slug or self.name:
            self.slug = slugify(str(self.name))
            if PropertyManagement.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.name)) + '-' + str(randint(1, 9999999))
        super(PropertyManagement, self).save(*args, **kwargs)


    def __str__(self):
        return str(self.pk)

class PropertyImage(AbstractDateTimeFieldBaseModel):
    property_image       = models.FileField(_("Property Image"), upload_to=property_management_image, default=property_management_default_image, null=True, blank=True)
    property_management  = models.ForeignKey(PropertyManagement, related_name="property_images", on_delete=models.CASCADE, blank=True, null=True)
    uuid                 = models.CharField(_('UUID'),  max_length=150, editable=False, null=True, blank=True)
    
    def __str__(self):
        return self.uuid
    
    class Meta:
        verbose_name = "PropertyImage"
        verbose_name_plural = "PropertyImages"


class PropertyManagementCollection(AbstractDateTimeFieldBaseModel):
    property_management  = models.ForeignKey(PropertyManagement, related_name="property_management_collection", on_delete=models.CASCADE, blank=True, null=True)
    property_collection  = models.ForeignKey(PropertyCollection, related_name="property_collection", on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return self.property_management.name
    
    class Meta:
        verbose_name = "PropertyManagementCollection"
        verbose_name_plural = "PropertyManagementCollections"


class HotelRoom(AbstractDateTimeFieldBaseModel):
    slug                 = models.SlugField(_('Slug'), max_length=100, editable=False)
    room_type            = models.ForeignKey(RoomType, blank=True, related_name="property_room_type", on_delete=models.SET_NULL, null=True)
    description          = models.TextField(null=True,blank=True)
    room_size            = models.CharField(max_length=256, blank=True)
    price                = models.CharField(max_length=256, blank=True, null=True)
    room_count           = models.CharField(max_length=256, blank=True, null=True)
    
    class Meta:
        verbose_name = "HotelRoom"
        verbose_name_plural = "HotelRooms"
    
    # slug for Medications table with releated to name
    def save(self, *args, **kwargs):
        if not self.slug or self.description:
            self.slug = slugify(str(self.description))
            if HotelRoom.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.description)) + '-' + str(randint(1, 9999999))
        super(HotelRoom, self).save(*args, **kwargs)

    def __str__(self):
        return self.description
    
class HotelRoomPropertyFacility(AbstractDateTimeFieldBaseModel):
    slug              = models.SlugField(_('Slug'), max_length=100, editable=False,null=True, blank=True)
    property_facility = models.ForeignKey(PropertyFacility, related_name="property_management_property_facility", on_delete=models.SET_NULL, blank=True, null=True)
    hotel_room        = models.ForeignKey(HotelRoom, related_name="property_management_facility_hotel_room", on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        verbose_name = "HotelRoomPropertyFacility"
        verbose_name_plural = "HotelRoomPropertyFacility"
        
    # slug for Medications table with releated to name
    def save(self, *args, **kwargs):
        if not self.slug or self.property_facility.name:
            self.slug = slugify(str(self.property_facility.name))
            if HotelRoomPropertyFacility.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.property_facility.name)) + '-' + str(randint(1, 9999999))
        super(HotelRoomPropertyFacility, self).save(*args, **kwargs)

    def __str__(self):
        return self.property_facility.name
    
    
class RoomImage(AbstractDateTimeFieldBaseModel):
    room_image           = models.FileField(_("Room Image"), upload_to=property_management_image, default=property_management_default_image, null=True, blank=True)
    hotel_room           = models.ForeignKey(HotelRoom, related_name="hotel_room_image", on_delete=models.CASCADE, blank=True, null=True)
    uuid                 = models.CharField(_('Room Image UUID'),  max_length=150, editable=False, null=True, blank=True)
    
    def __str__(self):
        return self.hotel_room.room_type.name
    
    class Meta:
        verbose_name = "RoomImage"
        verbose_name_plural = "RoomImages"
        
class PropertyManagementHotelRoom(AbstractDateTimeFieldBaseModel):
    hotel_room           = models.ForeignKey(HotelRoom, related_name="property_management_hotel_room", on_delete=models.SET_NULL, blank=True, null=True)
    property_management  = models.ForeignKey(PropertyManagement, related_name="property_management_property_management", on_delete=models.CASCADE, blank=True, null=True)
    is_booked            = models.BooleanField(default=False)
    def __str__(self):
        return self.property_management.name
    
    class Meta:
        verbose_name = "PropertyManagementHotelRoom"
        verbose_name_plural = "PropertyManagementHotelRooms"
        
# End


def property_temporary_image_upload_image_dir(request):
    return 'assets/property_management/image/{}/{}.png'.format(request.user.id, uuid4())

def room_temporary_image_upload_image_dir(request):
    return 'assets/property_management/room/image/{}/{}.png'.format(request.user.id, uuid4())


# class PropertyRoomStockQuantity(AbstractDateTimeFieldBaseModel):
#     slug                  = models.SlugField(_('Slug'), max_length=100, editable=False,null=True, blank=True)
#     property_hotel        = models.ForeignKey(PropertyManagementHotelRoom, related_name="hotel_room_booking", on_delete=models.SET_NULL, blank=True, null=True)
#     remaining_quantity    = models.IntegerField()

#     class Meta:
#         verbose_name          = "PropertyManagementQuantity"
#         verbose_name_plural   = "PropertyManagementQuantity"
        
#     def save(self, *args, **kwargs):
#         if not self.slug or self.quantity:
#             self.slug = slugify(str(self.quantity))
#             if PropertyRoomStockQuantity.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
#                 self.slug = slugify(str(self.quantity)) + '-' + str(randint(1, 9999999))
#         super(PropertyRoomStockQuantity, self).save(*args, **kwargs)

