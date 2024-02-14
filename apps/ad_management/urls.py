from django.urls import path, re_path, include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'ad_management'

urlpatterns = [
    path('', login_required(views.AdManagementView.as_view()), name='ad_management.index'),
    path('create/', login_required(views.AdManagementCreateOrUpdateView.as_view()), name='ad_management.create'),
    path('<str:id>/update/', views.AdManagementCreateOrUpdateView.as_view(), name='ad_management.update'),
    path('ad-management-datatable', login_required(views.LoadAdManagementDatatable.as_view()), name='load.ad_management.datatable'),
    path('destroy_records/', login_required(views.DestroyAdManagementRecordsView.as_view()), name='ad_management.records.destroy'),
    path('active-or-inactive/', login_required(views.AdManagementStatusChange.as_view()), name="ad_management.status_change"),
]