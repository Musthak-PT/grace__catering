from rest_framework import generics, status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from apps.contactus.api.serializer import BePartnerSerializer,ContactUsSerializer
from solo_core.helpers.custom_messages import _success
from solo_core.response import ResponseInfo
from apps.contactus.models import PartnersLogo
from apps.contactus.api.schemas import GetPartnerImagesWebResponseSchemas

#Start Be a partner
class BeAPartnerEnquiryFromSubmissionApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(BeAPartnerEnquiryFromSubmissionApiView, self).__init__(**kwargs)
        
    serializer_class= BePartnerSerializer
    
    @swagger_auto_schema(tags=["Enquiry"])
    def post(self, request):
        try:
            serializer =self.serializer_class(data=request.data,context={'request':request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            self.response_format['status_code']= status.HTTP_201_CREATED
            self.response_format['data']=serializer.data
            self.response_format['message']=_success
            self.response_format['status']=True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#End
#Contact us
class ContactUsEnquiryFromSubmissionApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(ContactUsEnquiryFromSubmissionApiView, self).__init__(**kwargs)
        
    serializer_class= ContactUsSerializer
    
    @swagger_auto_schema(tags=["Enquiry"])
    def post(self, request):
        try:
            serializer =self.serializer_class(data=request.data,context={'request':request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            self.response_format['status_code']= status.HTTP_201_CREATED
            self.response_format['message']=_success
            self.response_format['data']=serializer.data
            self.response_format['status']=True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#End
#Partner logo
class GetAllPartnerLogoImagesWebAPIView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetAllPartnerLogoImagesWebAPIView, self).__init__(**kwargs)

    queryset         = PartnersLogo.objects.all().order_by('-id')  # Use all() to retrieve all instances
    serializer_class = GetPartnerImagesWebResponseSchemas

    @swagger_auto_schema(tags=["Partners Logo"])
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(queryset, many=True)

        self.response_format['status'] = True
        self.response_format['data']   = serializer.data
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)
#End
        