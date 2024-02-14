from django.shortcuts import render
from rest_framework import status, generics
from apps.bannerimage.api.schemas import GetBannerImagesWebResponseSchemas
from apps.bannerimage.models import BannerImages
from drf_yasg import openapi
from rest_framework import filters
from solo_core.helpers.response import ResponseInfo
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
# Banner image web section is started
class GetAllBannerImagesWebAPIView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetAllBannerImagesWebAPIView, self).__init__(**kwargs)

    queryset = BannerImages.objects.filter(banner_details__is_active=True).order_by('-id')
    serializer_class = GetBannerImagesWebResponseSchemas
    filter_backends = [filters.SearchFilter]
    search_fields = ['slug']

    id = openapi.Parameter('id', openapi.IN_QUERY,
                                type=openapi.TYPE_INTEGER, required=False, description="Enter id")

    @swagger_auto_schema(tags=["Banner Image(Web)"], manual_parameters=[id])
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        instance_id = request.GET.get('id', None)
        if instance_id:
            queryset = queryset.filter(pk=instance_id)
        serializer = self.serializer_class(queryset, context={'request': request}, many=True)
        
        self.response_format['status'] = True
        self.response_format['message'] = "success"
        self.response_format['data'] = serializer.data
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)
# End