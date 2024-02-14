from django.urls import path, re_path, include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'banner_image'

urlpatterns = [       
    re_path(r'^banner_image/', include([
        path('', login_required(views.BannerImageView.as_view()), name='banner_image.index'),
        path('create/', login_required(views.BannerImageCreateOrUpdateView.as_view()), name='banner_image.create'),
        path('<str:id>/update/', views.BannerImageCreateOrUpdateView.as_view(), name='banner_image.update'),
        path('banner-image-datatable', login_required(views.LoadBannerImageDatatable.as_view()), name='load.banner_image.datatable'),
        path('destroy_records/', login_required(views.DestroyBannerImageRecordsView.as_view()), name='banner_image.records.destroy'),
        path('active-or-inactive/', login_required(views.BannerImageStatusChange.as_view()), name="banner_image.status_change"),
        path('banner-image-upload', login_required(views.BannerImageUploadView.as_view()), name='banner_image.image.upload'),
        path('get-banner-images', views.GetBannerimagesView.as_view(), name='get.banner_images.images'),
    ])),
]