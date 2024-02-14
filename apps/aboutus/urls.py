from django.urls import path, re_path, include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'about_us'

urlpatterns = [       
    re_path(r'^about_us/', include([
        path('', login_required(views.AboutUsView.as_view()), name='about_us.index'),
        path('create/', login_required(views.AboutUsCreateOrUpdateView.as_view()), name='about_us.create'),
        path('<str:id>/update/', views.AboutUsCreateOrUpdateView.as_view(), name='about_us.update'),
        path('about-us-datatable', login_required(views.LoadAboutUsDatatable.as_view()), name='load.about_us.datatable'),
        path('destroy_records/', login_required(views.DestroyAboutUsRecordsView.as_view()), name='about_us.records.destroy'),
        path('active-or-inactive/', login_required(views.AboutUsStatusChange.as_view()), name="about_us.status_change"),
    ])),
]