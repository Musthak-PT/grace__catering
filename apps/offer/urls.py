from django.urls import path, re_path, include
from . import views
from django.contrib.auth.decorators import login_required
app_name = 'offer_management'

urlpatterns = [       
    re_path(r'^offer/', include([
        path('', login_required(views.OfferManagementView.as_view()), name='offer_management.view.index'),
        path('create/', login_required(views.OfferManagementCreateOrUpdateView.as_view()), name='offer_management.create'),
        path('<str:id>/update/', views.OfferManagementCreateOrUpdateView.as_view(), name='offer_management.update'),
        path('get-room/', views.GetRoomListView.as_view(), name='room_list.get'),
        path('load-offer-management-datatable', login_required(views.LoadOfferManagementDatatable.as_view()), name='load.offer_management.datatable'),
        # path('<str:id>/detail-view/', login_required(views.ContactUsEnquieryDetailViewView.as_view()), name='contact-us-enquiry.detail-view'),
        path('destroy_records/', login_required(views.DestroyOfferManagementRecordsView.as_view()), name='offer_management.records.destroy'),
        path('active-or-inactive/', login_required(views.OfferManagementStatusChange.as_view()), name="offer_management.status_change"),
    ])),
]