from django.urls import path, re_path, include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'user_management'

urlpatterns = [       
    re_path(r'^user_management/', include([
        path('', login_required(views.UserView.as_view()), name='user.index'),
        path('user', login_required(views.LoadUserDatatable.as_view()), name='load.user.datatable'),
        path('create/', login_required(views.UserCreateOrUpdateView.as_view()), name='user.create'),
        path('<str:id>/update/', views.UserCreateOrUpdateView.as_view(), name='user.update'),
        path('destroy_records/', login_required(views.DestroyUserRecordsView.as_view()), name='user.records.destroy'),
        path('active-or-inactive/', login_required(views.UserStatusChange.as_view()), name="user.status_change"),

    ])),
]