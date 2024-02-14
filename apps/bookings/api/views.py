from django.shortcuts import render
from rest_framework import status, generics
from apps.property_management.models import PropertyManagementHotelRoom
from solo_core.helpers.response import ResponseInfo
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from .serializers import BookingConfirmationSerializer
# Create your views here.

class BookingConfirmationApiView(generics.GenericAPIView):
    
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(BookingConfirmationApiView, self).__init__(**kwargs)
    
    serializer_class = BookingConfirmationSerializer
    @swagger_auto_schema(tags=["Room Booking(Web)"])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            
            assigned_user_contact = PropertyManagementHotelRoom.objects.filter(hotel_room_id=serializer.validated_data.get('bookingdetails')[0]['room_id'].id).first().property_management.address
            response = {
                "result":serializer.data,
                "mobile_number": str(assigned_user_contact.phone),
                "alter_native_mobile_number": str(assigned_user_contact.alternative_phone)
            }
            self.response_format['status_code']             = status.HTTP_201_CREATED
            self.response_format['data']                    = response
            self.response_format["message"]                 = "Success"
            self.response_format["status"]                  = True
            return Response(self.response_format, status    = status.HTTP_201_CREATED)

        except Exception as e:
            self.response_format['status_code']             = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status']                  = False
            self.response_format['message']                 = str(e)
            return Response(self.response_format, status    = status.HTTP_500_INTERNAL_SERVER_ERROR)