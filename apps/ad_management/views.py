from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.contrib import messages
from django.http import JsonResponse
from apps.property_management.models import PropertyManagement
from solo_core.helpers.signer import URLEncryptionDecryption
from uuid import uuid4
from django.db.models import Q
from .models import AdManagement
from datetime import datetime, timedelta
# Create your views here.


class AdManagementView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/ad-management/ad-management-list.html'
        self.context['title'] = 'Ad Management'
        self.generateBreadcrumbs()
        
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'), 'active' : False})
        self.context['breadcrumbs'].append({"name" : "Ad Management", "route" : '','active' : True})
        


class LoadAdManagementDatatable(BaseDatatableView):
    model = AdManagement
    order_columns = ['id']
    
    def get_initial_queryset(self):
        filter_start_date = self.request.POST.get('columns[4][search][value]', None)
        filter_end_date = self.request.POST.get('columns[5][search][value]', None)
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        queryset = self.model.objects.all().order_by('-id')
        if filter_start_date:
            start_date = datetime.strptime(filter_start_date, '%Y-%m-%d').date()
            queryset = queryset.filter(Q(created_date__gte=start_date))

        if filter_end_date:
            end_date = datetime.strptime(filter_end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(Q(created_date__lte=end_date + timedelta(days=1)))
            
        if filter_value == '1':
            return queryset.filter(is_active=True)
        elif filter_value == '2':
            return queryset.filter(is_active=False)
        elif filter_value == '3':
            return queryset.filter()
        else:
            return queryset.filter()
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(ad_title__istartswith=search))
        return qs

    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'              : escape(item.id),
                'title'           : escape(item.ad_title),
                'property_name'   : escape(item.property.name),
                'created_date'    : escape(item.created_date.strftime("%d-%m-%Y")),
                'image'           : escape(item.image.url),
                'is_active'       : escape(item.is_active),
                'encrypt_id'      : escape(URLEncryptionDecryption.enc(item.id)),
            })
        return json_data

class AdManagementCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.context = {"breadcrumbs": []}
        self.context['title'] = 'Ad Management'
        self.action = "Created"
        self.template = 'admin/home-page/ad-management/create-or-update-ad-management.html'

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        self.context['uuid'] = uuid4()
        if self.request.user.is_superuser:
            property_m_obj = PropertyManagement.objects.all()
        else:
            property_m_obj = PropertyManagement.objects.filter(assigned_to=self.request.user)
        self.context['property_query_set'] = property_m_obj
        if id:
            self.action = "Updated"
            self.context['ad_management_obj'] = get_object_or_404(AdManagement, id=id)
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
        self.context['breadcrumbs'].append(
            {"name": "Ad Management", "route": reverse('ad_management:ad_management.index'), 'active': False})
        self.context['breadcrumbs'].append({"name": "{} Ad Management".format(self.action), "route": '', 'active': True})

    def post(self, request, *args, **kwargs):
        ad_management_id    = request.POST.get('ad_management_id', None)
        
        try:
            if ad_management_id:
                self.action = 'Updated'
                ad_management_obj         = get_object_or_404(AdManagement, id=ad_management_id)
            else:
                ad_management_obj         = AdManagement()
            ad_management_obj.ad_title = request.POST.get('title')
            ad_management_obj.ad_description = request.POST.get('description')
            ad_management_obj.property_id = request.POST.get('property_name')
            
            if request.FILES.__len__() != 0:
                if request.POST.get('ad_image', None) is None:
                    ad_management_obj.image = request.FILES.get('ad_image')
            ad_management_obj.save()
            messages.success(request, f"Data Successfully "+ self.action)
            
        except Exception as e:
            messages.error(request, f"Something went wrong."+str(e))
            if ad_management_id is not None:
                return redirect('ad_management:ad_management.update', id=URLEncryptionDecryption.dec(int(ad_management_id)))
            return redirect('ad_management:ad_management.create')
        
        return redirect('ad_management:ad_management.index')


class DestroyAdManagementRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            ad_management_id = request.POST.getlist('ids[]')
            if ad_management_id:
                AdManagement.objects.filter(id__in=ad_management_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
            
        return JsonResponse(self.response_format, status=200)
    
    
class AdManagementStatusChange(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance    = AdManagement.objects.get(id = instance_id)
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