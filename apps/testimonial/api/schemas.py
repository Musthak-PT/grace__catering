from rest_framework import serializers
from apps.testimonial.models import Testimonial

class GetTestimonialWebResponseSchemas(serializers.ModelSerializer):
    
    class Meta:
        model  = Testimonial
        fields = ['id', 'slug', 'testimonial_title', 'testimonial_image','testimonial_fullname','testimonial_description']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas