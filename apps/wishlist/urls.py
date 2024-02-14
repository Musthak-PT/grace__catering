from django.urls import path, re_path, include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'wishlist'

urlpatterns = [       
    re_path(r'^wishlist/', include([
        path('', login_required(views.WishlistView.as_view()), name='wishlist.index'),
        # path('create/', login_required(views.WishlistCreateOrUpdateView.as_view()), name='wishlist.create'),
        # path('<str:id>/update/', views.WishlistCreateOrUpdateView.as_view(), name='wishlist.update'),
        path('wishlist-datatable', login_required(views.LoadWishlistDatatable.as_view()), name='load.wishlist.datatable'),
        # path('destroy_records/', login_required(views.DestroyWishlistRecordsView.as_view()), name='wishlist.records.destroy'),
        # path('active-or-inactive/', login_required(views.WishlistStatusChange.as_view()), name="wishlist.status_change"),
    ])),
]