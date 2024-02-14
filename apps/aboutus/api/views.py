from django.shortcuts import render
from rest_framework import status, generics
from apps.aboutus.api.schemas import GetAboutUsWebResponseSchemas
from apps.aboutus.models import AboutUs
from drf_yasg import openapi
from rest_framework import filters
from solo_core.helpers.response import ResponseInfo
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
# About Us web section is started
class GetAllAboutUsWebAPIView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetAllAboutUsWebAPIView, self).__init__(**kwargs)

    queryset         = AboutUs.objects.filter().order_by('-id')
    serializer_class = GetAboutUsWebResponseSchemas
    filter_backends  = [filters.SearchFilter]
    # permission_classes = [IsAuthenticated]
    search_fields    = ['slug', 'title', 'description',]

    id = openapi.Parameter('id', openapi.IN_QUERY,
                                type=openapi.TYPE_INTEGER, required=False, description="Enter id")

    @swagger_auto_schema(tags=["About Us"], manual_parameters=[id])
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
# End