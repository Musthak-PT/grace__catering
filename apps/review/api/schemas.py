from rest_framework import serializers
from apps.review.models import CustomerReview



"""--------------CustomerReview RESPONSE SCHEMAS---------------"""

class CustomerReviewListingApiSchemas(serializers.ModelSerializer):
    
    class Meta:
        model = CustomerReview
        fields = '__all__'
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data
