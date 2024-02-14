from rest_framework import  generics,status
from solo_core.helpers.response import ResponseInfo
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from apps.wishlist.api.serializers import WishListSerializer
from solo_core.helpers.custom_messages import _success
from rest_framework.permissions import IsAuthenticated
from apps.wishlist.models import WishList
from apps.wishlist.api.schemas import GetWishlistedPropertiesSchemas
from rest_framework import filters
from solo_core.helpers.pagination import RestPagination
from drf_yasg import openapi
from solo_core.helpers.helper import get_object_or_none

# Create your views here.
class WishlistCreateApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(WishlistCreateApiView, self).__init__(**kwargs)

    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Wishlist(Web)"])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            wishlist_entry = get_object_or_none(WishList, user=request.user.id, property=serializer.validated_data.get('property'))
            
            if wishlist_entry is not None:
                wishlist_entry.delete()
                message = "Removed from Wishlist"
            else:
                serializer.save()
                message = "Added to Wishlist"

            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = message
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)

        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# class WishlistCreateApiView(generics.GenericAPIView):
#     def __init__(self, **kwargs):
#         self.response_format = ResponseInfo().response
#         super(WishlistCreateApiView, self).__init__(**kwargs)

#     serializer_class = WishListSerializer
#     permission_classes = [IsAuthenticated]

#     @swagger_auto_schema(tags=["Wishlist(Web)"])
#     def post(self, request):
#         try:
#             serializer = self.serializer_class(data=request.data,context = {'request':request})
#             if not serializer.is_valid():
#                 self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
#                 self.response_format["status"] = False
#                 self.response_format["errors"] = serializer.errors
#                 return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

#             if not serializer.is_valid():
#                 self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
#                 self.response_format["status"] = False
#                 self.response_format["errors"] = serializer.errors
#                 return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
#             serializer.save()
#             self.response_format['status_code'] = status.HTTP_201_CREATED
#             self.response_format["message"] = _success
#             self.response_format["status"] = True
#             return Response(self.response_format, status=status.HTTP_201_CREATED)
        
#         except Exception as e:
#             self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
#             self.response_format['status'] = False
#             self.response_format['message'] = str(e)
#             return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#------End-----

# from rest_framework.permissions import IsAuthenticated
class ListingWishlistApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(ListingWishlistApiView, self).__init__(**kwargs)
    # response_format = ResponseInfo().response
    queryset            = WishList.objects.filter().order_by('-id')
    serializer_class    = GetWishlistedPropertiesSchemas
    pagination_class    = RestPagination
    filter_backends     = [filters.SearchFilter]
    search_fields       = ['name']

    @swagger_auto_schema(tags=["Wishlist(Web)"])
    def get(self, request, *args, **kwargs):
        user = request.user
        queryset = self.queryset.filter(user_id=user.id)
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)
        
