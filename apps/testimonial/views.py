from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q
from django.utils.html import escape
from apps.testimonial.models import Testimonial
from solo_core.helpers.signer import URLEncryptionDecryption
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.


# Start Testimonial
class TestimonialView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/testimonial/testimonial-list.html'
        self.context['title'] = 'Testimonial'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Testimonial ", "route" : '','active' : True})
        

class LoadTestimonialDatatable(BaseDatatableView):
    model = Testimonial
    order_columns = ['id', 'testimonial_title', 'testimonial_fullname', 'testimonial_description']
    
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return Testimonial.objects.all().order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(testimonial_title__istartswith=search)|Q(testimonial_description__istartswith=search)|Q(testimonial_fullname__istartswith=search))
        return qs

    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'                          : escape(item.id),
                # 'testimonial_title'           : escape(item.testimonial_title),
                'image'                       : escape(item.testimonial_image.url),
                'testimonial_fullname'        : escape(item.testimonial_fullname),
                'testimonial_description'     : escape(item.testimonial_description),
                'is_active'                   : escape(item.is_active),
                'encrypt_id'                  : escape(URLEncryptionDecryption.enc(item.id)),
            })
        return json_data
    

class TestimonialCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs": []}
        self.context['title'] = 'Testimonial'
        self.action = "Created"
        self.template = 'admin/home-page/testimonial/create-or-update-testimonial.html'

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Updated"
            self.context['testimonial_obj'] = get_object_or_404(Testimonial, id=id)
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
        self.context['breadcrumbs'].append(
            {"name": "Testimonial", "route": reverse('about_us:about_us.index'), 'active': False})
        self.context['breadcrumbs'].append({"name": "{} Testimonial ".format(self.action), "route": '', 'active': True})

    def post(self, request, *args, **kwargs):
       
        testimonial_id = request.POST.get('testimonial_id', None)
        try:
            if testimonial_id:
                self.action = 'Updated'
                testimonial_obj         = get_object_or_404(Testimonial, id=testimonial_id)
            else:
                testimonial_obj         = Testimonial()

            # testimonial_obj.testimonial_title       = request.POST.get('title')
            testimonial_obj.testimonial_fullname    = request.POST.get('full_name')
            testimonial_obj.testimonial_description = request.POST.get('description')
            if request.FILES.__len__() != 0:
                if request.POST.get('testimonial_image', None) is None:
                    testimonial_obj.testimonial_image = request.FILES.get('testimonial_image')
            testimonial_obj.save()
            
            messages.success(request, f"Data Successfully "+ self.action)
            
        except Exception as e:
            messages.error(request, f"Something went wrong."+str(e))
            if testimonial_id is not None:
                return redirect('testimonial:testimonial.update', id=URLEncryptionDecryption.dec(int(testimonial_id)))
            return redirect('testimonial:testimonial.create')
        return redirect('testimonial:testimonial.index')


class DestroyTestimonialRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            testimonial_id = request.POST.getlist('ids[]')
            if testimonial_id:
                Testimonial.objects.filter(id__in=testimonial_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
            
        return JsonResponse(self.response_format, status=200)
    
    
class TestimonialStatusChange(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance    = Testimonial.objects.get(id = instance_id)
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
    
# End Testimonial us