from rest_framework import serializers
from apps.contactus.models import PartnersLogo

#Listing partners logo
class GetPartnerImagesWebResponseSchemas(serializers.ModelSerializer):
    
    class Meta:
        model  = PartnersLogo
        fields = ['partner_logo_image']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas