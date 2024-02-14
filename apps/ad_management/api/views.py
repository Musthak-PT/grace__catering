from rest_framework import status, generics
from apps.ad_management.api.schemas import GetAdImagesWebResponseSchemas
from apps.ad_management.models import AdManagement
from drf_yasg import openapi
from rest_framework import filters
from solo_core.helpers.response import ResponseInfo
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from solo_core.helpers.pagination import RestPagination
# Create your views here.
# Advertisement listing
class GetAdImagesWebAPIView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetAdImagesWebAPIView, self).__init__(**kwargs)

    queryset            = AdManagement.objects.filter(is_active=True).order_by('-id')
    serializer_class    = GetAdImagesWebResponseSchemas
    pagination_class    = RestPagination
    filter_backends     = [filters.SearchFilter]
    search_fields       = ['slug']

    id = openapi.Parameter('id', openapi.IN_QUERY,
                                type=openapi.TYPE_INTEGER, required=False, description="Enter id")

    @swagger_auto_schema(tags=["Ad Management(Web)"], manual_parameters=[id])
    def get(self, request, *args, **kwargs):
        queryset    = self.filter_queryset(self.get_queryset())
        instance_id = request.GET.get('id', None)
        if instance_id:
            queryset = queryset.filter(pk=instance_id)

        page          = self.paginate_queryset(queryset)
        serializer    = self.serializer_class(page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)
# End