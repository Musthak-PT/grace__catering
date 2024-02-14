from rest_framework import status, generics
from apps.testimonial.api.schemas import GetTestimonialWebResponseSchemas
from apps.testimonial.models import Testimonial
from drf_yasg import openapi
from rest_framework import filters
from solo_core.helpers.response import ResponseInfo
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from apps.testimonial.api.serializers import TestimonialSerializer

# Create your views here.
class TestimonialCreateApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(TestimonialCreateApiView, self).__init__(**kwargs)

    serializer_class=TestimonialSerializer
    @swagger_auto_schema(tags=["Testimonial(Web)"])

    def post(self, request): 
        try:
            testimonialid=request.data.get('testimonialid',None)

            if testimonialid is not None and testimonialid:
                testimonialid=Testimonial.objects.get(id=testimonialid) 
                serializer = self.serializer_class(testimonialid, data=request.data, context={'request': request})
            else:
                serializer = self.serializer_class(data=request.data, context={'request': request})

            if not serializer.is_valid():
                self.response_format['status_code']   = status.HTTP_400_BAD_REQUEST,
                self.response_format['status']        = False,
                self.response_format['errors']        = serializer.errors,
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()

            self.response_format['status_code']             = status.HTTP_201_CREATED,
            self.response_format['status']                  = True,
            self.response_format['message']                 = "Success",
            self.response_format['data']                    = serializer.data,
            return Response(self.response_format, status    = status.HTTP_201_CREATED)

        except Exception as e:            
            self.response_format['status_code']   = status.HTTP_500_INTERNAL_SERVER_ERROR,
            self.response_format['status']        = False,
            self.response_format['errors']        = str(e),
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# testimonial web section is started
class GetAllTestimonialWebAPIView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetAllTestimonialWebAPIView, self).__init__(**kwargs)

    queryset         = Testimonial.objects.filter(is_active=True).order_by('-id')
    serializer_class = GetTestimonialWebResponseSchemas
    filter_backends  = [filters.SearchFilter]
    search_fields    = ['slug', 'testimonial_title','full_name','description']

    id = openapi.Parameter('id', openapi.IN_QUERY,
                                type=openapi.TYPE_INTEGER, required=False, description="Enter id")

    @swagger_auto_schema(tags=["Testimonial(Web)"], manual_parameters=[id])
    def get(self, request, *args, **kwargs):
        queryset    = self.filter_queryset(self.get_queryset())
        instance_id = request.GET.get('id', None)
        if instance_id:
            queryset = queryset.filter(pk=instance_id)
        serializer = self.serializer_class(queryset, many=True,context={'request': request})
        
        self.response_format['status'] = True
        self.response_format['data']   = serializer.data
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)    
# End