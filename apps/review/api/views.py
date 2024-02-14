import logging
from rest_framework.response import Response
from rest_framework import generics, status
from drf_yasg.utils import swagger_auto_schema
from apps.customers.promotion_email import auto_review_mail_send
from apps.property_management.models import PropertyManagementHotelRoom
from apps.review.api.schemas import CustomerReviewListingApiSchemas
from apps.review.models import CustomerReview
from solo_core.response import ResponseInfo
logger = logging.getLogger(__name__)
from rest_framework import filters
from solo_core.helpers.custom_messages import _success
from rest_framework.permissions import IsAuthenticated
from apps.review.api.serializers import AddedReviewSerializer, ReviewSerializer
from drf_yasg import openapi
from django.db.models import Q
from datetime import datetime
from apps.bookings.models import HotelRoomBookingBookingPrice
from django.http import JsonResponse
from solo_core.helpers.signer import URLEncryptionDecryption

#Creating customer review
class CreateCustomerReviewWebApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreateCustomerReviewWebApiView, self).__init__(**kwargs)

    serializer_class    = ReviewSerializer
    permission_classes  = [IsAuthenticated]

    @swagger_auto_schema(tags=["Customer Review"])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data,context = {'request':request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            self.response_format['status_code']             = status.HTTP_201_CREATED
            self.response_format['data']                    = serializer.data
            self.response_format["message"]                 = _success
            self.response_format["status"]                  = True
            return Response(self.response_format, status    = status.HTTP_201_CREATED)
        
        except Exception as e:
            self.response_format['status_code']             = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status']                  = False
            self.response_format['message']                 = str(e)
            return Response(self.response_format, status    = status.HTTP_500_INTERNAL_SERVER_ERROR)
#End
#Get all customer review
class GetCustomerReviewWebApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetCustomerReviewWebApiView, self).__init__(**kwargs)

    serializer_class = CustomerReviewListingApiSchemas
    filter_backends = [filters.SearchFilter]
    search_fields = ['customer_name', 'title', 'description']

    property_id = openapi.Parameter('property_id', openapi.IN_QUERY,
                                    type=openapi.TYPE_INTEGER, required=False, description="Enter id of Property:")

    @swagger_auto_schema(tags=["Customer Review"], manual_parameters=[property_id])
    def get(self, request, *args, **kwargs):
        queryset = CustomerReview.objects.filter().order_by('-id')
        property_id = request.GET.get('property_id', None)

        if property_id:
            try:
                property_id = int(property_id)
            except ValueError:
                # Handle the case where property_id is not a valid integer
                pass
            else:
                # Use Q objects to filter by property_id
                queryset = queryset.filter(Q(property__id=property_id))
        price_booking_obj = HotelRoomBookingBookingPrice.objects.filter(Q(booked_room__check_out__date=datetime.now().date()))
        print("L####################################", price_booking_obj)
        auto_review_mail_send(price_booking_obj)
    
        queryset = self.filter_queryset(queryset)
        serializer = self.serializer_class(queryset, many=True)

        self.response_format['status']                  = True
        self.response_format['data']                    = serializer.data
        self.response_format['status_code']             = status.HTTP_200_OK
        return Response(self.response_format, status    = status.HTTP_200_OK)


class CustomerAddReviewView(generics.GenericAPIView):
    
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CustomerAddReviewView, self).__init__(**kwargs)
    
    serializer_class = AddedReviewSerializer
    
    @swagger_auto_schema(tags=["Customer Review"])
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, context = {'request':request})
            if serializer.is_valid():
                enc_id                 = serializer.validated_data.get('enc_id', None)
                title                  = serializer.validated_data.get('title', None)
                description            = serializer.validated_data.get('description', None)
                rating                 = serializer.validated_data.get('rating', None)
                dec_id                 = URLEncryptionDecryption.dec(enc_id)
                hotel_room_obj         = HotelRoomBookingBookingPrice.objects.filter(id=dec_id).first()
                property_obj           = PropertyManagementHotelRoom.objects.filter(hotel_room=hotel_room_obj.booked_room.room_id).first()
                
                review_obj = CustomerReview(
                    user        = hotel_room_obj.booked_price.customer_details,
                    property    = property_obj.property_management,
                    rating      = rating,
                    description = description,
                    title       = title,
                )
                review_obj.save()
                self.response_format['status_code']             = status.HTTP_201_CREATED
                self.response_format['data']                    = serializer.data
                self.response_format["message"]                 = _success
                self.response_format["status"]                  = True
                return Response(self.response_format, status    = status.HTTP_201_CREATED)
            
            self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
            self.response_format["status"] = False
            self.response_format["errors"] = serializer.errors
            return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.response_format['status_code']             = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status']                  = False
            self.response_format['message']                 = str(e)
            return Response(self.response_format, status    = status.HTTP_500_INTERNAL_SERVER_ERROR)
#End 
#End
