from solo_core.helpers.helper import ConvertBase64File
from uuid import uuid4
from rest_framework import serializers
from apps.wishlist.models import WishList
from apps.property_management.models import PropertyManagement
from solo_core.helpers.helper import get_object_or_none
from solo_core.helpers.helper import get_token_user_or_none
from apps.review.models import CustomerReview
from django.shortcuts import get_object_or_404
from apps.users.models import Users
#creation of rating and review
class ReviewSerializer(serializers.ModelSerializer):
    property              = serializers.PrimaryKeyRelatedField(queryset=PropertyManagement.objects.all(),required=True)
    rating                = serializers.CharField()
    description           = serializers.CharField()
    title                 = serializers.CharField()
    image                 = serializers.CharField(required=False)

    class Meta:
        model =  CustomerReview
        fields = ['property','rating','description','title','image']   

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):        
        request = self.context.get('request')
        instance = CustomerReview()
        instance.user_id          = request.user.id
        fist_name_object          = get_object_or_404(Users, id=request.user.id)
        instance.customer_name    = fist_name_object.first_name
        instance.property         = validated_data.get('property')
        instance.rating           = validated_data.get('rating')
        instance.description      = validated_data.get('description')
        instance.title            = validated_data.get('title')
        instance.image            = validated_data.get('image')
        image                     = validated_data.pop('image', None)
        if image:
            request = self.context.get('request')
            extension           = ConvertBase64File.base64_file_extension(image)
            output_schema_xsd   = ConvertBase64File.base64_to_file(image)
            unique_filename     = f'{uuid4()}.{extension}'                    
            instance.image.save(unique_filename, output_schema_xsd, save = True)
        instance.save()
        return instance


class AddedReviewSerializer(serializers.Serializer):
    enc_id                = serializers.CharField()
    title                 = serializers.CharField()
    description           = serializers.CharField()
    rating                = serializers.CharField()
    

#End