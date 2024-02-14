import logging
from django.contrib import messages
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.urls import reverse
from django.utils.html import escape
from django.http import JsonResponse
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from apps.review.models import CustomerReview
from solo_core.helpers.signer import URLEncryptionDecryption
logger = logging.getLogger(__name__)





"""--------------------- CustomerReview Management-------------------------------"""

class CustomerReviewView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/customer-review/listing.html' 
        self.context['title'] = 'Customer Review'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Customer Review", "route" : '','active' : True})
        
        
class CustomerReviewDatatable(BaseDatatableView):
    order_columns = ['id', 'user', 'customer_name', 'property', 'rating', 'description', 'title'] 
    
    def get_initial_queryset(self):
        if self.request.user.is_superuser:
            reviews = CustomerReview.objects.all()
        else:
            reviews = CustomerReview.objects.filter(property__assigned_to=self.request.user)
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return reviews.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return reviews.filter(is_active=False).order_by('-id')
        else:
            return reviews.order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(title__istartswith=search)|Q(description__istartswith=search))
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'            : escape(item.id),
                'encrypt_id'    : escape(URLEncryptionDecryption.enc(item.id)),
                'full_name'     : escape(item.user.full_name),
                'property'      : escape(item.property.name),
                'title'         : escape(item.title),
                'rating'        : escape(item.rating),
                'description'   : escape(item.description),
                'is_active'     : escape(item.is_active),
            })
        return json_data


@method_decorator(login_required, name='dispatch')
class DestroyCustomerReviewRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                CustomerReview.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)
    
    
class ActiveInactiveCustomerReview(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = CustomerReview.objects.get(id = instance_id)
            if instance_id:
                if instance.is_active:
                    instance.is_active = False
                else:
                    instance.is_active =True
                instance.save()
                self.response_format['status_code']=200
                self.response_format['message']= 'Success'
                
        except Exception as es:
            self.response_format['message']='error'
            self.response_format['error'] = str(es)
        return JsonResponse(self.response_format, status=200)
    

class CustomerReviewCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : [],}
        self.action = "Create"
        self.context['title'] = 'Customer Review'
        self.template = 'admin/home-page/customer-review/create-or-update.html' 

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Update"
            self.context['instance'] = get_object_or_404(CustomerReview, id=id)
        
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)
    
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Customer Review", "route" : reverse('review:customer_review-view.index') ,'active' : False})
        self.context['breadcrumbs'].append({"name" : "{} Customer Review ".format(self.action), "route" : '','active' : True})

    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('instance_id', None)
        
        try:
            if instance_id:
                self.action = 'Updated'
                instance = get_object_or_404(CustomerReview, id=instance_id)
                instance.updated_by = request.user
            else:
                instance = CustomerReview()

            if request.FILES.get('image', None) is not None:
                instance.image       = request.FILES.get('image',None)

            instance.customer_name    = request.POST.get('customer_name',None)
            instance.designation      = request.POST.get('designation',None)
            instance.review           = request.POST.get('review',None)
            instance.rating           = request.POST.get('rating',None)
            instance.created_by       = request.user
            instance.save()
            
            messages.success(request, f"Data Successfully " + self.action)
            
        except Exception as e:
            messages.error(request, f"Something went wrong."+str(e))
            if instance_id is not None and instance_id != '':
                return redirect('review:customer_review.update', id = URLEncryptionDecryption.dec(int(instance_id)) )   
            return redirect('review:customer_review.create')
        return redirect('review:customer_review-view.index')