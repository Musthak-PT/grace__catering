from rest_framework import serializers
from apps.bookings.models import RoomBookedCustomerDetails

class GetBookedCustomerDetailsExcelDownloadSchemas(serializers.ModelSerializer):
    
    class Meta:
        model  = RoomBookedCustomerDetails
        fields = ['full_name', 'email_address','mobile_number','dob','guest_address']