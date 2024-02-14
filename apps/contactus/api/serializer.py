from rest_framework import serializers
from apps.contactus.api.contact_us_mail import be_a_partner_form_submits_mail_send , contact_us_form_submits_mail_send
from apps.contactus.models import ContactUs

#Be a partner
class BePartnerSerializer(serializers.ModelSerializer):
    enquiry_type    = serializers.CharField(required=True)
    name            = serializers.CharField(required=True)
    email           = serializers.CharField(required=True)
    mobile_number   = serializers.CharField(required=True)
    state           = serializers.CharField(required=True)

    class Meta:
        model = ContactUs
        fields=['enquiry_type','name','email','mobile_number','state']

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        request                   = self.context.get('request')
        instance                  = ContactUs()
        instance.enquiry_type     = validated_data.get('enquiry_type',None)
        instance.name             = validated_data.get('name',None)
        instance.email            = validated_data.get('email',None)
        instance.mobile_number    = validated_data.get('mobile_number',None)
        instance.state            = validated_data.get('state',None)
        instance.save()
        be_a_partner_form_submits_mail_send(request,instance)
        return instance
#End
#Contact us
class ContactUsSerializer(serializers.ModelSerializer):
    enquiry_type    = serializers.CharField(required=True)
    message         = serializers.CharField(required=True)
    name            = serializers.CharField(required=True)
    email           = serializers.CharField(required=True)

    class Meta:
        model = ContactUs
        fields=['enquiry_type','message','name','email']

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        request                 = self.context.get('request')
        instance                = ContactUs()
        instance.enquiry_type   = validated_data.get('enquiry_type',None)
        instance.message        = validated_data.get('message',None)
        instance.name           = validated_data.get('name',None)
        instance.email          = validated_data.get('email',None)
        instance.save()
        contact_us_form_submits_mail_send(request, instance)
        return instance
#End
