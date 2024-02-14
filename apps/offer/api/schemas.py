from rest_framework import serializers
from apps.offer.models import PropertyOffer
from apps.property_management.models import *


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id','property_image']

class GetAllPropertyOfferPropertSchemas(serializers.ModelSerializer):
    property_slug = serializers.CharField(source='room_property.property_management.slug')
    
    class Meta:
        model  = PropertyOffer
        fields = ['id', 'slug', 'title', 'description', 'image', 'property_slug']




class GetAllPropertyOfferSchemas(serializers.ModelSerializer):
    property_slug = serializers.CharField(source='room_property.property_management.slug')
    
    class Meta:
        model  = PropertyOffer
        fields = ['id', 'slug', 'title', 'description', 'image', 'property_slug']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas