from rest_framework import serializers
from apps.aboutus.models import AboutUs

class GetAboutUsWebResponseSchemas(serializers.ModelSerializer):
    
    class Meta:
        model  = AboutUs
        fields = ['id', 'slug', 'title', 'description']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas