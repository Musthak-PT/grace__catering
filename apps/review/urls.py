from django.urls import path,re_path,include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'review'

urlpatterns = [

    re_path(r'^customer-review/', include([
        path('', login_required(views.CustomerReviewView.as_view()), name='customer_review-view.index'),
        path('load-customer-review_datatable', login_required(views.CustomerReviewDatatable.as_view()), name='load.customer_review.datatable'),
        path('active/', login_required(views.ActiveInactiveCustomerReview.as_view()), name="active.or.inactive.customer_review"),
        path('create/',login_required(views.CustomerReviewCreateOrUpdateView.as_view()), name='customer_review.create'),
        path('<str:id>/update/', login_required(views.CustomerReviewCreateOrUpdateView.as_view()), name='customer_review.update'),
        path('destroy_records/', login_required(views.DestroyCustomerReviewRecordsView.as_view()), name='customer_review.records.destroy'),
    ])),
    
]

