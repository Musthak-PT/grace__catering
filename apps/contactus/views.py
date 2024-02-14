import logging
from django.contrib import messages
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.shortcuts import get_object_or_404, render,redirect
from django.views import View
from django.urls import reverse
from django.utils.html import escape
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from apps.contactus.models import ContactUs
from solo_core.helpers.signer import URLEncryptionDecryption
logger = logging.getLogger(__name__)
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone

"""----------------------CONTACT US LISTING-------------------"""

class ContactUsEnquieryView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/contact-us/contact-us-listing/contactus-listing.html'  
        self.context['title'] = 'Contact Us'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Contact Us", "route" : '','active' : True})


class LoadContactUsEnquieryDatatable(BaseDatatableView):
    model = ContactUs
    order_columns = ['id'] 
    
    def get_initial_queryset(self):

        filter_start_date = self.request.POST.get('columns[4][search][value]', None)
        filter_end_date = self.request.POST.get('columns[5][search][value]', None)
        filter_value = self.request.POST.get('columns[3][search][value]', None)

        queryset = self.model.objects.filter(enquiry_type='1').order_by('-id')
        if filter_start_date:
            start_date = datetime.strptime(filter_start_date, '%Y-%m-%d').date()
            queryset = queryset.filter(Q(created_date__gte=start_date))

        if filter_end_date:
            end_date = datetime.strptime(filter_end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(Q(created_date__lte=end_date + timedelta(days=1)))

        
        if filter_value == '1':
            return queryset.filter(is_contacted=False)
        elif filter_value == '2':
            return queryset.filter(is_contacted=True)
        elif filter_value == '3':
            return queryset.filter()
        else:
            return queryset.filter()
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(email__istartswith=search)|Q(name__istartswith=search) |Q(message__istartswith=search))
        return qs
    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'              : escape(item.id),
                'name'            : escape(item.name),
                'email'           : escape(item.email),
                'message'         : escape(item.message),
                'created_date'    : timezone.localtime(item.created_date).strftime("%Y-%m-%d %H:%M:%S"),
                'is_contacted'    : escape(item.is_contacted),
                'encrypt_id'      : escape(URLEncryptionDecryption.enc(item.id)),
            })
        return json_data


@method_decorator(login_required, name='dispatch')
class DestroyContactUsEnquieryRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                ContactUs.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)


class ContactUsEnquiryContactedStatusChange(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = ContactUs.objects.get(id = instance_id)
            if instance_id:
                if instance.is_contacted:
                    instance.is_contacted = False
                else:
                    instance.is_contacted =True
                instance.save()
                self.response_format['status_code']=200
                self.response_format['message']= 'Success'
                
        except Exception as es:
            self.response_format['message']='error'
            self.response_format['error'] = str(es)
        return JsonResponse(self.response_format, status=200)



class ContactUsEnquieryDetailViewView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs": [],}
        self.action = "Created"
        self.context['title'] = 'Contact Us'
        self.template = 'admin/home-page/contact-us/contact-us-listing/contact-us-detail.html'

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Detail View"
            self.context['instance'] = get_object_or_404(ContactUs, id=id)

        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
        self.context['breadcrumbs'].append({"name": "Contact Us", "route": reverse('contact:contact-us-enquiry.view.index'), 'active': False})
        self.context['breadcrumbs'].append({"name": "{}".format(self.action), "route": '', 'active': True})
        
        
# End

# Start Be a partner

class PartnerEnquieryView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/contact-us/partner-enquiry/partner-enquiry-listing.html'  
        self.context['title'] = 'Be A Partner'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Be A Partner", "route" : '','active' : True})


class LoadPartnerEnquieryDatatable(BaseDatatableView):
    model = ContactUs
    order_columns = ['id', 'name', 'email', 'mobile_number','state','created_date']
    
    def get_initial_queryset(self):
        filter_start_date = self.request.POST.get('columns[4][search][value]', None)
        filter_end_date = self.request.POST.get('columns[5][search][value]', None)
        filter_value = self.request.POST.get('columns[3][search][value]', None)

        queryset = self.model.objects.filter(enquiry_type='2').order_by('-id')
        if filter_start_date:
            start_date = datetime.strptime(filter_start_date, '%Y-%m-%d').date()
            queryset = queryset.filter(Q(created_date__gte=start_date))

        if filter_end_date:
            end_date = datetime.strptime(filter_end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(Q(created_date__lte=end_date + timedelta(days=1)))

        
        if filter_value == '1':
            return queryset.filter(is_contacted=False)
        elif filter_value == '2':
            return queryset.filter(is_contacted=True)
        elif filter_value == '3':
            return queryset.filter()
        else:
            return queryset.filter()
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(email__istartswith=search)|Q(full_name__istartswith=search)|Q(mobile_number__istartswith=search))
        return qs
    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'              : escape(item.id),
                'full_name'       : escape(item.name),
                'email'           : escape(item.email),
                'mobile_number'   : escape(item.mobile_number),
                'state'           : escape(item.state),
                'created_date'    : timezone.localtime(item.created_date).strftime("%Y-%m-%d %H:%M:%S"),
                'is_contacted'    : escape(item.is_contacted),
                'encrypt_id'      : escape(URLEncryptionDecryption.enc(item.id)),
            })
        return json_data


@method_decorator(login_required, name='dispatch')
class DestroyContactUsEnquieryRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                ContactUs.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)


class ContactUsEnquiryContactedStatusChange(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = ContactUs.objects.get(id = instance_id)
            if instance_id:
                if instance.is_contacted:
                    instance.is_contacted = False
                else:
                    instance.is_contacted =True
                instance.save()
                self.response_format['status_code']=200
                self.response_format['message']= 'Success'
                
        except Exception as es:
            self.response_format['message']='error'
            self.response_format['error'] = str(es)
        return JsonResponse(self.response_format, status=200)
    
# End
