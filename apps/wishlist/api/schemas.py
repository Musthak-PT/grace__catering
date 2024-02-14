from rest_framework import serializers
from apps.property_management.models import *
from apps.wishlist.models import WishList
from apps.offer.models import PropertyOffer
from django.db.models import Q

class WishlistPropertyImageListSchema(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id','property_image']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data:
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data

class WishlistPropertyAddressListSchema(serializers.ModelSerializer):
    class Meta:
        model = PropertyAddress
        fields = ['id','street','city']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data:
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data

class WishlistPropertyFacilityListSchema(serializers.ModelSerializer):
    class Meta:
        model = PropertyFacility
        fields = ['name']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data:
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data

class PropertyManagementSerializer(serializers.ModelSerializer):
    image           = serializers.SerializerMethodField('get_image')
    address         = serializers.SerializerMethodField('get_address')
    facility        = serializers.SerializerMethodField('get_facility')
    has_offer       = serializers.SerializerMethodField('get_has_offer')
    is_wishlisted   = serializers.SerializerMethodField('get_is_wishlisted')
    
    class Meta:
        model = PropertyManagement
        fields = ['slug','id', 'image', 'name', 'address', 'facility','has_offer','is_wishlisted','location_distance']

    def get_is_wishlisted(self, instance):
        request = self.context.get('request')       
        wishlist_obj = WishList.objects.filter(Q(property_id=instance.id) & Q(user_id=request.user.id)).exists()
        return wishlist_obj


    def get_image(self, instance):
        request = self.context.get('request')
        image_obj = PropertyImage.objects.filter(property_management_id=instance.id)
        image_schema = WishlistPropertyImageListSchema(image_obj, many=True, context={'request': request})
        return image_schema.data

    def get_address(self, instance):
        address_obj = instance.address
        if address_obj:
            address_schema = WishlistPropertyAddressListSchema(address_obj)
            return address_schema.data
        else:
            return None

    def get_facility(self, instance):
        hotel_room_ids = PropertyManagementHotelRoom.objects.filter(
            property_management=instance
        ).values_list('hotel_room', flat=True)

        property_facility_instances = HotelRoomPropertyFacility.objects.filter(
            hotel_room__in=hotel_room_ids
        ).values_list('property_facility', flat=True)

        facility_names = PropertyFacility.objects.filter(
            id__in=property_facility_instances
        ).values_list('name', flat=True).distinct()

        return facility_names
    def get_has_offer(self, instance):
        # Check if there is an offer for this PropertyManagement
        has_offer = PropertyOffer.objects.filter(
            room_property__property_management=instance
        ).exists()
        return has_offer
    
class GetWishlistedPropertiesSchemas(serializers.ModelSerializer):
    property = PropertyManagementSerializer()
    class Meta:
        model  = WishList
        fields = ['id','property']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas