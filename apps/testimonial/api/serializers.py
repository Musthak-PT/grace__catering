from rest_framework import serializers
from apps.testimonial.models import Testimonial
from solo_core.helpers.helper import ConvertBase64File
from uuid import uuid4
#creating serializers for Testimonial
class TestimonialSerializer(serializers.ModelSerializer): 
    testimonial_title       = serializers.CharField()
    testimonial_image       = serializers.CharField()
    testimonial_fullname    = serializers.CharField()
    testimonial_description = serializers.CharField()

    class Meta: 
        model     = Testimonial
        fields    = ['testimonial_title','testimonial_image','testimonial_fullname','testimonial_description']
        
    def validate(self, attrs): 
        return super().validate(attrs)
    
    def create(self, validated_data): 
        instance                            = Testimonial()
        instance.testimonial_title          = validated_data.get('testimonial_title')
        instance.testimonial_image          = validated_data.get('testimonial_image')
        instance.testimonial_fullname       = validated_data.get('testimonial_fullname')
        instance.testimonial_description    = validated_data.get('testimonial_description')
        testimonial_image                   = validated_data.pop('testimonial_image',None)
        if testimonial_image:
            request = self.context.get('request')
            extension           = ConvertBase64File.base64_file_extension(request,testimonial_image)
            output_schema_xsd   = ConvertBase64File.base64_to_file(request,testimonial_image)
            unique_filename     = f'{uuid4()}.{extension}'
            instance.testimonial_image.save(unique_filename, output_schema_xsd, save = True)
        instance.save()
        return instance