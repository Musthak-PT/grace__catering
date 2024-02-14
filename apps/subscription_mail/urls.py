from django.urls import path, re_path, include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'subscription'

urlpatterns = [       
    re_path(r'^subscription/', include([
        path('', login_required(views.SubscriptionlistView.as_view()), name='subscription.index'),
        path('subscription-datatable', login_required(views.LoadSubscriptionDatatable.as_view()), name='load.subscription.datatable'),
    ])),
]