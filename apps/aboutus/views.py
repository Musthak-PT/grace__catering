from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q
from django.utils.html import escape
from solo_core.helpers.signer import URLEncryptionDecryption
from django.contrib import messages
from django.http import JsonResponse
from .models import AboutUs

# start About us
class AboutUsView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/about_us/about-us-list.html'
        self.context['title'] = 'About Us'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "About Us", "route" : '','active' : True})
        

class LoadAboutUsDatatable(BaseDatatableView):
    model = AboutUs
    order_columns = ['id', 'title', 'description']
    
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return AboutUs.objects.all().order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(title__istartswith=search)|Q(description__istartswith=search))
        return qs

    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'              : escape(item.id),
                'title'           : escape(item.title),
                'description'     : escape(item.description),
                'is_active'       : escape(item.is_active),
                'encrypt_id'      : escape(URLEncryptionDecryption.enc(item.id)),
            })
        return json_data
    

class AboutUsCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.context = {"breadcrumbs": []}
        self.context['title'] = 'About Us'
        self.action = "Create"
        self.template = 'admin/home-page/about_us/create-or-update-about-us.html'

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))

        if id:
            self.action = "Update "
            self.context['about_us_obj'] = get_object_or_404(AboutUs, id=id)
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
        self.context['breadcrumbs'].append(
            {"name": "About Us", "route": reverse('about_us:about_us.index'), 'active': False})
        self.context['breadcrumbs'].append({"name": "{} About Us".format(self.action), "route": '', 'active': True})

    def post(self, request, *args, **kwargs):
        about_us_id = request.POST.get('about_us_id', None)
        try:
            if about_us_id:
                self.action = 'Updated'
                about_us_obj         = get_object_or_404(AboutUs, id=about_us_id)
            else:
                about_us_obj         = AboutUs()

            about_us_obj.title       = request.POST.get('title')
            about_us_obj.description = request.POST.get('description')
            about_us_obj.save()
            
            messages.success(request, f"Data Successfully "+ self.action)
            
        except Exception as e:
            messages.error(request, f"Something went wrong."+str(e))
            if about_us_id is not None:
                return redirect('about_us:about_us.update', id=URLEncryptionDecryption.dec(int(about_us_id)))
            return redirect('about_us:about_us.create')
        return redirect('about_us:about_us.index')


class DestroyAboutUsRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            about_us_id = request.POST.getlist('ids[]')
            if about_us_id:
                AboutUs.objects.filter(id__in=about_us_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
            
        return JsonResponse(self.response_format, status=200)
    
    
class AboutUsStatusChange(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance    = AboutUs.objects.get(id = instance_id)
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
    
# End About us