from pprint import pprint
from django.shortcuts import render
from rest_framework import status, generics
from apps.property_management.api.schemas import *
from apps.property_management.api.serializers import *
from apps.property_management.models import *
from drf_yasg import openapi
from rest_framework import filters
from solo_core.helpers.response import ResponseInfo
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from solo_core.helpers.pagination import RestPagination
from django.db.models import Q
from solo_core.helpers.custom_messages import _success
from solo_core.helpers.helper import get_object_or_none
from apps.users.models import Users
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from django.http import JsonResponse
import sys,os


# Create your views here.
# AccommodationType is started
class GetAllAccommodationTypeWebAPIView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetAllAccommodationTypeWebAPIView, self).__init__(**kwargs)

    queryset         = AccommodationType.objects.filter().order_by('-id')
    serializer_class = GetAccommodationTypeUsWebResponseSchemas
    filter_backends  = [filters.SearchFilter]
    fields = ['id', 'slug', 'name', 'description']

    id = openapi.Parameter('id', openapi.IN_QUERY,
                                type=openapi.TYPE_INTEGER, required=False, description="Enter id")
    
    @swagger_auto_schema(tags=["Property management(Web)"], manual_parameters=[id])
    def get(self, request, *args, **kwargs):
        queryset    = self.filter_queryset(self.get_queryset())
        instance_id = request.GET.get('id', None)
        if instance_id:
            queryset = queryset.filter(pk=instance_id)
        serializer = self.serializer_class(queryset, many=True)
        
        self.response_format['status'] = True
        self.response_format['data']   = serializer.data
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)    
# End AccommodationType

# PropertyCollection is started
class GetAllPropertyCollectionWebAPIView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetAllPropertyCollectionWebAPIView, self).__init__(**kwargs)

    queryset         = PropertyCollection.objects.filter().order_by('-id')
    serializer_class = GetPropertyCollectionWebResponseSchemas
    filter_backends  = [filters.SearchFilter]
    fields = ['id', 'slug', 'name', 'description']

    id = openapi.Parameter('id', openapi.IN_QUERY,
                                type=openapi.TYPE_INTEGER, required=False, description="Enter id")

    @swagger_auto_schema(tags=["Property management(Web)"], manual_parameters=[id])
    def get(self, request, *args, **kwargs):
        queryset    = self.filter_queryset(self.get_queryset())
        instance_id = request.GET.get('id', None)
        if instance_id:
            queryset = queryset.filter(pk=instance_id)
        serializer = self.serializer_class(queryset, many=True)
        
        self.response_format['status'] = True
        self.response_format['data']   = serializer.data
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)    
# End PropertyCollection

# PropertyFacility is started
class GetAllPropertyFacilityWebAPIView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetAllPropertyFacilityWebAPIView, self).__init__(**kwargs)

    queryset         = PropertyFacility.objects.filter().order_by('-id')
    serializer_class = GetPropertyFacilityWebResponseSchemas
    filter_backends  = [filters.SearchFilter]
    fields = ['id', 'slug', 'name', 'description']

    id = openapi.Parameter('id', openapi.IN_QUERY,
                                type=openapi.TYPE_INTEGER, required=False, description="Enter id")

    @swagger_auto_schema(tags=["Property management(Web)"], manual_parameters=[id])
    def get(self, request, *args, **kwargs):
        queryset    = self.filter_queryset(self.get_queryset())
        instance_id = request.GET.get('id', None)
        if instance_id:
            queryset = queryset.filter(pk=instance_id)
        serializer = self.serializer_class(queryset, many=True)
        
        self.response_format['status'] = True
        self.response_format['data']   = serializer.data
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)    
# End PropertyFacility
# Start
class GetPropertyFilteringWebAPIView(generics.GenericAPIView):
    
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetPropertyFilteringWebAPIView, self).__init__(**kwargs)
    
    queryset            = PropertyManagement.objects.filter().order_by('-id')
    serializer_class    = PropertyFilteringSerializer
    serializer          = FilterPropertyManagementSchema
    pagination_class    = RestPagination
    filter_backends     = [filters.SearchFilter]
    search_fields       = ['name']

    
    @swagger_auto_schema(tags=["Property management(Web)"])
    def post(self, request):
        room_type_name          = request.data.get('room_type', None)
        minimum_price           = request.data.get('minimum_price', None)
        maximum_price           = request.data.get('maximum_price', None)
        place                   = request.data.get('place', None)
        property_facility_id    = request.data.get('property_facility_id', None)
        accomadation_type       = request.data.get('accomadation_type', None)
        collection_type         = request.data.get('collection_type', None)
        sorting_type            = request.data.get('sorting_type', None)
        check_in                = request.data.get('check_in', None)
        check_out               = request.data.get('check_out', None)

        queryset = self.get_queryset()

        if room_type_name:
            room_list = list(HotelRoom.objects.filter(room_type_id__in=room_type_name).values_list('id', flat=True))
            property_room_type_obj = list(PropertyManagementHotelRoom.objects.filter(hotel_room_id__in=room_list).values_list('property_management', flat=True).distinct())
            queryset = queryset.filter(id__in=property_room_type_obj)
        
        # if minimum_price and maximum_price:
        #     queryset = queryset.filter(Q(total_price__gte=minimum_price) & 
        #                                Q(total_price__lte=maximum_price))
        if place:
            queryset = queryset.filter(Q(address__street__icontains=place))
        
        if property_facility_id:
            hotel_room_ids = HotelRoomPropertyFacility.objects.filter(property_facility_id__in=property_facility_id).values_list('hotel_room', flat=True)
            property_ids = PropertyManagementHotelRoom.objects.filter(hotel_room__in=hotel_room_ids).values_list('property_management', flat=True).distinct()
            queryset = queryset.filter(id__in=property_ids)
        
        if accomadation_type:
            accomadation_id = PropertyManagement.objects.filter(accomodation_type_id__in=accomadation_type).values_list("id",flat=True)
            queryset = queryset.filter(id__in=accomadation_id)
        
        if collection_type:
            property_management_id = PropertyManagementCollection.objects.filter(property_collection_id__in=collection_type).values_list('property_management',flat=True)
            queryset = queryset.filter(id__in=property_management_id)
        
        # if sorting_type:
        #     if sorting_type == 'LowtoHigh':
        #         queryset = queryset.order_by('total_price')
        #     elif sorting_type == 'HightoLow':
        #         queryset = queryset.order_by('-total_price')
                        
        if check_in and check_out:
            booked_rooms = HotelRoomBooking.objects.filter(
                Q(check_in__lte=check_in, check_out__gte=check_in) |
                Q(check_in__lte=check_out, check_out__gte=check_out) |
                Q(check_in__gte=check_in, check_out__lte=check_out)
            ).values_list('room_id', flat=True)
            queryset = queryset.exclude(id__in=booked_rooms)
        
        if not check_in or not check_out:
            current_date = datetime.now().date()
            check_in = current_date
            check_out = current_date + timedelta(days=1)
        
        search_term = request.data.get('search')
        if search_term:
            queryset = queryset.filter(name__icontains=search_term)
        page = self.paginate_queryset(queryset)
        serializer = self.serializer(page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)   
#End
#Start collection dropdown
class GetCollectionDropdownApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetCollectionDropdownApiView, self).__init__(**kwargs)

    queryset         = PropertyCollection.objects.filter().order_by('-id')
    serializer_class = GetDropdowncollectionSchemas
    filter_backends  = [filters.SearchFilter]

    @swagger_auto_schema(tags=["Property management(Web)"])
    def get(self, request, *args, **kwargs):
        
        queryset    = self.filter_queryset(self.get_queryset())
        instance_id = request.GET.get('id', None)
        if instance_id :
            queryset = queryset.filter(pk=instance_id)
            
        serializer   = self.serializer_class(queryset, many=True)
        
        self.response_format['status']      = True
        self.response_format['data']        = serializer.data
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)
#End
#Start Accomadation dropdown
class GetAccomadationTypeDropdownApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetAccomadationTypeDropdownApiView, self).__init__(**kwargs)

    queryset         = AccommodationType.objects.filter().order_by('-id')
    serializer_class = GetDropdownAccomadationTypeSchemas
    filter_backends  = [filters.SearchFilter]

    @swagger_auto_schema(tags=["Property management(Web)"])
    def get(self, request, *args, **kwargs):
        
        queryset    = self.filter_queryset(self.get_queryset())
        instance_id = request.GET.get('id', None)
        if instance_id :
            queryset = queryset.filter(pk=instance_id)
            
        serializer   = self.serializer_class(queryset, many=True)
        
        self.response_format['status']      = True
        self.response_format['data']        = serializer.data
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)
#End
class GetPropertyRoomTypesDropdownApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetPropertyRoomTypesDropdownApiView, self).__init__(**kwargs)

    queryset         = RoomType.objects.filter().order_by('-id')
    serializer_class = GetDropdownPropertyRoomTypeSchemas
    filter_backends  = [filters.SearchFilter]

    @swagger_auto_schema(tags=["Property management(Web)"])
    def get(self, request, *args, **kwargs):
        
        queryset    = self.filter_queryset(self.get_queryset())
        instance_id = request.GET.get('id', None)
        if instance_id :
            queryset = queryset.filter(pk=instance_id)
            
        serializer   = self.serializer_class(queryset, many=True)
        
        self.response_format['status']      = True
        self.response_format['data']        = serializer.data
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)
#Start Property Facility dropdown
class GetPropertyFacilityDropdownApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetPropertyFacilityDropdownApiView, self).__init__(**kwargs)

    queryset         = PropertyFacility.objects.filter().order_by('-id')
    serializer_class = GetDropdownPropertyFacilitySchemas
    filter_backends  = [filters.SearchFilter]

    @swagger_auto_schema(tags=["Property management(Web)"])
    def get(self, request, *args, **kwargs):
        
        queryset    = self.filter_queryset(self.get_queryset())
        instance_id = request.GET.get('id', None)
        if instance_id :
            queryset = queryset.filter(pk=instance_id)
            
        serializer   = self.serializer_class(queryset, many=True)
        
        self.response_format['status']      = True
        self.response_format['data']        = serializer.data
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)
#End
#property detailed view
class GetPropertyDetailedApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetPropertyDetailedApiView, self).__init__(**kwargs)

    queryset         = PropertyManagement.objects.filter().order_by('-id')
    serializer_class = GetPropertyDetailedViewSchemas
    filter_backends  = [filters.SearchFilter]
    search_fields    = ['slug']

    
    slug = openapi.Parameter('slug', openapi.IN_QUERY,
                        type=openapi.TYPE_STRING, required=False, description="Enter slug")

    @swagger_auto_schema(tags=["Property management(Web)"], manual_parameters=[slug])
    def get(self, request, *args, **kwargs):
        queryset    = self.filter_queryset(self.get_queryset())
        instance_id = request.GET.get('slug', None)
        if instance_id:
            queryset = queryset.filter(slug=instance_id)
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        
        self.response_format['status']                  = True
        self.response_format['data']                    = serializer.data
        self.response_format['status_code']             = status.HTTP_200_OK
        return Response(self.response_format, status    = status.HTTP_200_OK)
# End
#Room booking api view
class CreateRoomBookingApiView(generics.GenericAPIView):
    
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreateRoomBookingApiView, self).__init__(**kwargs)
    
    serializer_class = RoomBookingSerializer
    
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
            
            self.response_format['status_code']             = status.HTTP_201_CREATED
            self.response_format['data']                    = serializer.data
            self.response_format["message"]                 = "Success"
            self.response_format["status"]                  = True
            return Response(self.response_format, status    = status.HTTP_201_CREATED)

        except Exception as e:
            self.response_format['status_code']             = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status']                  = False
            self.response_format['message']                 = str(e)
            return Response(self.response_format, status    = status.HTTP_500_INTERNAL_SERVER_ERROR)
#End
# Get the room booked customer profile details
class GetRoomBookingProfileApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetProfileDetailsSchemas
    filter_backends = [filters.SearchFilter]
    search_fields = ['slug']

    @swagger_auto_schema(tags=["Room Booking(Web)"])
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(queryset, many=True, context={'request': request})

        response_format                           = ResponseInfo().response
        response_format['status']                 = True
        response_format['data']                   = serializer.data
        response_format['status_code']            = status.HTTP_200_OK
        return Response(response_format, status   = status.HTTP_200_OK)

    def get_queryset(self):
        return Users.objects.filter(pk=self.request.user.pk).order_by('-id')
 
#End
#Room selection api view
class GetRoomSelectionApiView(generics.GenericAPIView):

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetRoomSelectionApiView, self).__init__(**kwargs)

    queryset            = PropertyManagementHotelRoom.objects.filter().order_by('-id')
    serializer_class    = RoomSelectionSerializer
    schema              = RoomSelectionSchema
    pagination_class    = RestPagination
    filter_backends     = [filters.SearchFilter]

    @swagger_auto_schema(tags=["Room Booking(Web)"])
    def post(self, request):
        property_id = request.data.get('property', None)
        room_type = request.data.get('room_type', None)
        check_in = request.data.get('check_in', None)
        check_out = request.data.get('check_out', None)

        queryset = self.get_queryset()

        if property_id is not None:
            queryset = queryset.filter(property_management_id=property_id)

        hotel_rooms = HotelRoom.objects.filter(property_management_hotel_room__in=queryset)

        if room_type:
            hotel_rooms = hotel_rooms.filter(room_type=room_type)
        page = self.paginate_queryset(hotel_rooms)
        serializer = self.schema(page, many=True, context={"request": request,"check_in":check_in,"check_out":check_out})
        return self.get_paginated_response(serializer.data)
#End
# create or Update the profile details of booked customer
# class CreateOrUpdateBookedProfileApiView(generics.GenericAPIView): 
#     def __init__(self, **kwargs):
#         self.response_format = ResponseInfo().response
#         super(CreateOrUpdateBookedProfileApiView, self).__init__(**kwargs)

#     serializer_class = CreateUpdateBookedProfileSerializer

#     @swagger_auto_schema(tags= ["Property management(Web)"])

#     def post(self, request): 
#         try : 
#             serializer                                          = self.serializer_class(data=request.data, context={'request': request})

#             if not serializer.is_valid(): 
#                 self.response_format['status_code']             = status.HTTP_400_BAD_REQUEST,
#                 self.response_format['status']                  = False,
#                 self.response_format['errors']                  = serializer.errors,
#                 return Response(self.response_format, status    = status.HTTP_400_BAD_REQUEST)
            
#             serializer.save()
            
#             booking_confirmed_mail_send(request, )
#             self.response_format['status_code']             = status.HTTP_201_CREATED,
#             self.response_format['status']                  = True,
#             self.response_format['data']                    = serializer.data,
#             self.response_format['message']                 = "Success",
#             return Response(self.response_format, status    = status.HTTP_201_CREATED)
        
#         except Exception as e: 
#             self.response_format['status_code']             = status.HTTP_500_INTERNAL_SERVER_ERROR,
#             self.response_format['status']                  = False,
#             self.response_format['errors']                  = str(e),
#             return Response(self.response_format, status    = status.HTTP_500_INTERNAL_SERVER_ERROR)
#End
#----------------------------------------------------------------------

class GetMyBookingPropertiesApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetMyBookingPropertiesApiView, self).__init__(**kwargs)

    queryset = RoomBookedCustomerDetails.objects.filter().order_by('-id')
    serializer_class = GetMyBookingPropertiesSchemas
    filter_backends = [filters.SearchFilter]

    @swagger_auto_schema(tags=["Room Booking(Web)"])
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        instance_id = request.GET.get('id', None)
        
        if instance_id:
            queryset = queryset.filter(pk=instance_id)

        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        data = serializer.data

        # Filter out entries where both check_in_and_out and property_details are empty
        data = [entry for entry in data if entry['booked_details'] or entry['property_details']]

        self.response_format['status'] = True
        self.response_format['data'] = data
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)
    
#Detailed view of booked property
class GetMyBookingPropertiesDetailedApiView(generics.GenericAPIView):

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetMyBookingPropertiesDetailedApiView, self).__init__(**kwargs)

    queryset            = RoomBookedCustomerDetails.objects.filter().order_by('-id')
    serializer_class    = MyBookingPropertiesDetailedSerializer
    schema              = MyBookingPropertiesDetailedSchema
    pagination_class    = RestPagination
    filter_backends     = [filters.SearchFilter]

    @swagger_auto_schema(tags=["Room Booking(Web)"])
    def post(self, request):
        room_booked_details = request.data.get('room_booked_details', None)

        queryset = self.get_queryset()

        if room_booked_details is not None:
            queryset = queryset.filter(id=room_booked_details)

        page = self.paginate_queryset(queryset)
        serializer = self.schema(page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)
    
#Choose your room
# class GetChoosingRoomsApiView(generics.GenericAPIView):

#     def __init__(self, **kwargs):
#         self.response_format = ResponseInfo().response
#         super(GetChoosingRoomsApiView, self).__init__(**kwargs)

#     queryset            = PropertyManagementHotelRoom.objects.filter().order_by('-id')
#     serializer_class    = ChooseRoomSelectionSerializer
#     schema              = ChooseRoomSelectionSchema
#     pagination_class    = RestPagination
#     filter_backends     = [filters.SearchFilter]

#     @swagger_auto_schema(tags=["Room Booking(Web)"])
#     def post(self, request):
#         property_id = request.data.get('property', None)
#         room_type = request.data.get('room_type', None)
#         check_in = request.data.get('check_in', None)
#         check_out = request.data.get('check_out', None)

#         queryset = self.get_queryset()

#         if property_id is not None:
#             queryset = queryset.filter(property_management_id=property_id)

#         hotel_rooms = HotelRoom.objects.filter(property_management_hotel_room__in=queryset)

#         if room_type:
#             hotel_rooms = hotel_rooms.filter(room_type=room_type)
#         page = self.paginate_queryset(hotel_rooms)
#         serializer = self.schema(page, many=True, context={"request": request,"check_in":check_in,"check_out":check_out})
#         return self.get_paginated_response(serializer.data)
    

# class CreateAndListRoomBookingApiView(generics.GenericAPIView):
    
#     def __init__(self, **kwargs):
#         self.response_format = ResponseInfo().response
#         super(CreateAndListRoomBookingApiView, self).__init__(**kwargs)
    
#     serializer_class = HotelRoomBookingSerializer
    
#     @swagger_auto_schema(tags=["Room Booking(Web)"])
#     def post(self, request):
#         try:
#             # Deserialize and validate input data
#             serializer = self.serializer_class(data=request.data, context={'request': request})
#             if not serializer.is_valid():
#                 self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
#                 self.response_format["status"] = False
#                 self.response_format["errors"] = serializer.errors
#                 return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

#             # Create a new instance using the validated data
#             instance = sse_format["data"] = serialized_data  # Include serialized data in the response
#             return Response(self.response_format, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
#             self.response_format['status'] = False
#             self.response_format['message'] = str(e)
#             return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)erializer.save()

#             # Serialize the instance data
#             serialized_data = GetProfileDetailsSchemas(instance, context={"request": request}).data

#             self.response_format['status_code'] = status.HTTP_201_CREATED
#             self.response_format["message"] = _success
#             self.response_format["status"] = True
#             self.respon


class CreateAndListRoomBookingApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreateAndListRoomBookingApiView, self).__init__(**kwargs)
        
    serializer_class = HotelRoomBookingSerializer
    @swagger_auto_schema(tags=["Room Booking(Web)"])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
          
            serializer1 = BookingDetailesSchema(serializer.validated_data, context={"request": request})
            
            self.response_format['status'] = True
            self.response_format['data']   = serializer1.data
            self.response_format['status_code'] = status.HTTP_200_OK
            return Response(self.response_format, status=status.HTTP_200_OK)   
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(f'{exc_type}, {fname}, {exc_tb.tb_lineno}, {str(e)}')
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
