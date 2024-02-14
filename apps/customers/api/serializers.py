from rest_framework import serializers

class BookedCustomerDetailsExcelDownloadSerializer(serializers.Serializer):
    from_date   = serializers.DateField(required=True)
    to_date     = serializers.DateField(required=True)