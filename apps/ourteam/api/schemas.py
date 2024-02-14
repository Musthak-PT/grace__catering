from rest_framework import serializers
from apps.ourteam.models import OurTeam

class GetOuTeamWebResponseSchemas(serializers.ModelSerializer):
    
    class Meta:
        model  = OurTeam
        fields = ['id', 'slug', 'fullname', 'designation','image']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas