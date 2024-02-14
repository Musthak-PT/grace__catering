from rest_framework import serializers
from apps.bannerimage.models import BannerImages

class GetBannerImagesWebResponseSchemas(serializers.ModelSerializer):
    
    class Meta:
        model  = BannerImages
        fields = ['id', 'slug', 'image']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas