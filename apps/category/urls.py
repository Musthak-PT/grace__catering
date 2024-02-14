from django.urls import path, re_path, include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'category'

urlpatterns = [       
    re_path(r'^category/', include([
        path('', login_required(views.CategoryView.as_view()), name='category.index'),
        path('create/', login_required(views.CategoryCreateOrUpdateView.as_view()), name='category.create'),
        path('<str:id>/update/', views.CategoryCreateOrUpdateView.as_view(), name='category.update'),
        path('category', login_required(views.LoadCategoryDatatable.as_view()), name='load.category.datatable'),
        path('destroy_records/', login_required(views.DestroyCategoryRecordsView.as_view()), name='category.records.destroy'),
        path('active-or-inactive/', login_required(views.CategoryStatusChange.as_view()), name="category.status_change"),
        # path('banner-image-upload', login_required(views.BannerImageUploadView.as_view()), name='banner_image.image.upload'),
        # path('get-banner-images', views.GetBannerimagesView.as_view(), name='get.banner_images.images'),
    ])),
]