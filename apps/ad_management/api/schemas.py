from rest_framework import serializers
from apps.ad_management.models import AdManagement


class GetAdImagesWebResponseSchemas(serializers.ModelSerializer):
    property_slug = serializers.CharField(source='property.slug')
    class Meta:
        model  = AdManagement
        fields = ['id', 'slug', 'ad_title', 'ad_description', 'image', 'property_slug']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas