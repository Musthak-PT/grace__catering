from django.urls import path, re_path, include
from . import views
from django.contrib.auth.decorators import login_required


app_name = 'testimonial'

urlpatterns = [       
    re_path(r'^testimonial/', include([
        path('', login_required(views.TestimonialView.as_view()), name='testimonial.index'),
        path('create/', login_required(views.TestimonialCreateOrUpdateView.as_view()), name='testimonial.create'),
        path('<str:id>/update/', views.TestimonialCreateOrUpdateView.as_view(), name='testimonial.update'),
        path('testimonial-datatable', login_required(views.LoadTestimonialDatatable.as_view()), name='load.testimonial.datatable'),
        path('destroy_records/', login_required(views.DestroyTestimonialRecordsView.as_view()), name='testimonial.records.destroy'),
        path('active-or-inactive/', login_required(views.TestimonialStatusChange.as_view()), name="testimonial.status_change"),
    ])),
]