from rest_framework import serializers
from apps.wishlist.models import WishList
from apps.property_management.models import PropertyManagement
from solo_core.helpers.helper import get_object_or_none
from solo_core.helpers.helper import get_token_user_or_none

#--------------------wishlisting and unwishlist--------
class WishListSerializer(serializers.ModelSerializer):

    property   = serializers.PrimaryKeyRelatedField(queryset=PropertyManagement.objects.all(),required=True)

    class Meta:
        model =  WishList
        fields = ['property']   

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):        
        request = self.context.get('request')
        instance = WishList()
        wishlist_entry= get_object_or_none(WishList,user = request.user.id,property = validated_data.get('property'))
        if wishlist_entry is not None:
            wishlist_entry.delete()
        else:
            instance.property = validated_data.get('property')
            instance.user = get_token_user_or_none(request)
            instance.save()
        return instance
# End