from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q
from django.utils.html import escape
from apps.bannerimage.models import BannerImages, BannerImagesDetail, banner_temporary_image_upload_image_dir
from solo_core.helpers.signer import URLEncryptionDecryption
from django.contrib import messages
from django.http import JsonResponse
import uuid, os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from urllib.parse import urlparse
import json
from solo_core.helpers.helper import ConvertBase64File
from uuid import uuid4
# Create your views here.

# start About us
class BannerImageView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/banner-image/banner-image-list.html'
        self.context['title'] = 'Banner Image'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Banner Image", "route" : '','active' : True})
        

class LoadBannerImageDatatable(BaseDatatableView):
    model = BannerImagesDetail
    order_columns = ['id','title']
    
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return BannerImagesDetail.objects.all().order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(title__istartswith=search))
        return qs

    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'              : escape(item.id),
                'title'           : escape(item.title),
                'is_active'       : escape(item.is_active),
                'encrypt_id'      : escape(URLEncryptionDecryption.enc(item.id)),
            })
        return json_data
    

class BannerImageCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.context = {"breadcrumbs": []}
        self.context['title'] = 'Banner Image'
        self.action = "Create"
        self.template = 'admin/home-page/banner-image/create-or-update-banner-image.html'

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        self.context['uuid'] = uuid.uuid4()
        if id:
            self.action = "Update"
            self.context['banner_image_obj'] = get_object_or_404(BannerImagesDetail, id=id)
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
        self.context['breadcrumbs'].append(
            {"name": "Banner Image", "route": reverse('about_us:about_us.index'), 'active': False})
        self.context['breadcrumbs'].append({"name": "{} Banner Image".format(self.action), "route": '', 'active': True})

    def post(self, request, *args, **kwargs):
        banner_image_id    = request.POST.get('banner_image_id', None)
        banner_image_uuid  = request.POST.get('banner_image_uuid', None)
        banner_image_files = request.POST.get('banner_image_files', None)
        try:
            if banner_image_id:
                self.action = 'Updated'
                banner_image_obj         = get_object_or_404(BannerImagesDetail, id=banner_image_id)
                BannerImages.objects.filter(banner_details_id = banner_image_obj).delete()
            else:
                banner_image_obj         = BannerImagesDetail()
            banner_image_obj.title       = request.POST.get('title')
            banner_image_obj.save()
            image_string = banner_image_files.strip('[""]')

            image_list = image_string.split('","')
            
            for img in image_list:
                banner_obj = BannerImages()
                extension           = ConvertBase64File().base64_file_extension(img)
                output_schema_xsd   = ConvertBase64File().base64_to_file(img)
                unique_filename     = f'{uuid4()}.{extension}'
                banner_obj.banner_details = banner_image_obj         
                banner_obj.image.save(unique_filename, output_schema_xsd, save = True)
                banner_obj.save()
                
            messages.success(request, f"Data Successfully "+ self.action)
            
        except Exception as e:
            messages.error(request, f"Something went wrong."+str(e))
            if banner_image_id is not None:
                return redirect('banner_image:banner_image.update', id=URLEncryptionDecryption.dec(int(banner_image_id)))
            return redirect('banner_image:banner_image.create')
        
        return redirect('banner_image:banner_image.index')


class DestroyAboutUsRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            about_us_id = request.POST.getlist('ids[]')
            if about_us_id:
                BannerImages.objects.filter(id__in=about_us_id).delete()
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
            instance    = BannerImages.objects.get(id = instance_id)
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
    
    
class BannerImageUploadView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}
        
    def post(self, request, *args, **kwargs):
        try:
            instance_id = 0
            if request.FILES.__len__() != 0:
                image = request.FILES.get('file')
                uuid  = request.POST.get('uuid', None)
                banner_image = BannerImages()
                banner_image.uuid = uuid
                path = default_storage.save(banner_temporary_image_upload_image_dir(request), ContentFile(image.read()))
                banner_image.image = path
                banner_image.save()
                instance_id = banner_image.id
                
            self.response_format['status_code'] = 200
            self.response_format['message'] = 'Success'
            self.response_format['data'] = instance_id
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)
    
    
class GetBannerimagesView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": "", "data" : []}
    def post(self, request, *args, **kwargs):
        try:
            banner_id = request.POST.get('banner_image_id')
            if banner_id:
                banner_images_obj = BannerImages.objects.filter(banner_details_id=banner_id)
                json_data = []
                for item in banner_images_obj:
                    json_data.append({
                        'id'         : escape(item.id), 
                        'image'      : escape(request.build_absolute_uri(item.image.url)), 
                        'image_name' : escape(os.path.basename(urlparse(request.build_absolute_uri(item.image)).path)), 
                        'size'       : escape(item.image.size), 
                    })
                    
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
                self.response_format['data'] = json_data
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
            
        return JsonResponse(self.response_format, status=200)   


class BannerImageStatusChange(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance    = BannerImagesDetail.objects.get(id = instance_id)
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

class DestroyBannerImageRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            banner_image_id = request.POST.getlist('ids[]')
            if banner_image_id:
                BannerImagesDetail.objects.filter(id__in=banner_image_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
            
        return JsonResponse(self.response_format, status=200)
# End About us