from rest_framework import generics, status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from apps.subscription_mail.api.serializers import SubscriptionMailSerializer
from solo_core.helpers.custom_messages import _success
from solo_core.response import ResponseInfo
from apps.subscription_mail.api.subscription_mail_send import subscription_mail_send

#Subscription mail sending
class SubscriptionMailApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(SubscriptionMailApiView, self).__init__(**kwargs)
        
    serializer_class= SubscriptionMailSerializer
    
    @swagger_auto_schema(tags=["SubscriptionMail(Web)"])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            instance = serializer.save()

            subscription_mail_send(request, instance)

            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format['data']=serializer.data
            self.response_format['message'] = _success
            self.response_format['status'] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#End
