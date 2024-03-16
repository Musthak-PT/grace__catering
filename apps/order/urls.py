from django.urls import path, re_path, include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'order'

urlpatterns = [       
    re_path(r'^order/', include([
        path('', login_required(views.OrderView.as_view()), name='order.index'),
        path('create/', login_required(views.OrderCreateOrUpdateView.as_view()), name='order.create'),
        path('<str:id>/update/', views.OrderCreateOrUpdateView.as_view(), name='order.update'),
        path('order', login_required(views.LoadOrderDatatable.as_view()), name='load.order.datatable'),
        path('destroy_records/', login_required(views.DestroyorderRecordsView.as_view()), name='order.records.destroy'),
        path('active-or-inactive/', login_required(views.OrderStatusChange.as_view()), name="order.status_change"),

        path('OrderPrintDetailsView/', login_required(views.OrderPrintDetailsView.as_view()), name="order.OrderPrintDetailsView"),
    ])),
]