from rest_framework import serializers
from apps.subscription_mail.models import *

#Subscription mail sending
class SubscriptionMailSerializer(serializers.ModelSerializer):
    subscribers_email    = serializers.CharField(required=True,)

    class Meta:
        model = SubscribersList
        fields=['subscribers_email']

    # def validate(self, attrs):
    #     return super().validate(attrs)
    def validate_subscribers_email(self, value):
       
        if SubscribersList.objects.filter(subscribers_email=value).exists():
            raise serializers.ValidationError("This email is already subscribed.")
        return value

    def create(self, validated_data):
        request                       = self.context.get('request')
        instance                      = SubscribersList()
        instance.subscribers_email    = validated_data.get('subscribers_email',None)
        instance.save()
        return instance
#End