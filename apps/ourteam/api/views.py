from django.shortcuts import render
from rest_framework import status, generics
from apps.ourteam.api.schemas import GetOuTeamWebResponseSchemas
from apps.ourteam.models import OurTeam
from drf_yasg import openapi
from rest_framework import filters
from solo_core.helpers.response import ResponseInfo
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
# OurTeam web section is started
class GetAllOurTeamWebAPIView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetAllOurTeamWebAPIView, self).__init__(**kwargs)

    queryset         = OurTeam.objects.filter().order_by('-id')
    serializer_class = GetOuTeamWebResponseSchemas
    filter_backends  = [filters.SearchFilter]
    search_fields    = ['slug', 'fullname', 'designation']

    id = openapi.Parameter('id', openapi.IN_QUERY,
                                type=openapi.TYPE_INTEGER, required=False, description="Enter id")

    @swagger_auto_schema(tags=["Our Team(Web)"], manual_parameters=[id])
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