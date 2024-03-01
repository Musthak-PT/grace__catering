from solo_core.helpers.mail_fuction import SendEmails
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q
from django.utils.html import escape
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
from apps.users.models import Users
from concurrent.futures import ThreadPoolExecutor
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
class UserView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/user-management/user-listing.html'  
        self.context['title'] = 'Users'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Users", "route" : '','active' : True})

class LoadUserDatatable(BaseDatatableView):
    model = Users
    order_columns = ['id'] 

    def get_initial_queryset(self):


        queryset = self.model.objects.filter(user_type='2')


        filter_value = self.request.POST.get('columns[3][search][value]', None)

        if filter_value == '1':
            queryset = queryset.filter(is_active=True)
        elif filter_value == '2':
            queryset = queryset.filter(is_active=False)

        return queryset.order_by('-id')
        
        
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(first_name__istartswith=search)|Q(last_name__istartswith=search)|Q(email__istartswith=search))
        return qs

    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'            : escape(item.id),
                'first_name'    : escape(item.first_name),
                'last_name'     : escape(item.last_name),
                'email'         : escape(item.email),
                'phone'         : escape(item.phone),
                # 'date_joined'   : escape(item.date_joined.strftime("%d-%m-%Y")),
                'is_active'     : escape(item.is_active),
                'encrypt_id'    : escape(URLEncryptionDecryption.enc(item.id)),

            })
        return json_data
    
class UserCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs": []}
        self.action = "Create"
        self.context['title'] = 'User'
        self.template = 'admin/home-page/user-management/user-create-or-update.html'

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Update"
            self.context['instance'] = get_object_or_404(Users, id=id)

        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
        self.context['breadcrumbs'].append({"name": "{} User".format(self.action), "route": '', 'active': True})

    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('instance_id', None)
        try:
            if instance_id:
                self.action = 'Updated'
                instance = get_object_or_404(Users, id=instance_id)
                instance.updated_by = request.user
            else:
                instance = Users()
                self.action = 'Created'
                instance.user_type = '2'
                
            instance.first_name = request.POST.get('first_name', None)
            instance.last_name = request.POST.get('last_name', None)
            instance.phone = request.POST.get('phone', None)
            instance.email = request.POST.get('email', None)

            if not instance_id:
                # For new users, encrypt and save the password
                password = request.POST.get('password')
                if password:
                    instance.password = make_password(password)
            else:
                # For updates, check if a new password is provided and update it
                new_password = request.POST.get('password')
                if new_password:
                    instance.password = make_password(new_password)

            instance.created_by = request.user
            instance.save()

            messages.success(request, f"Data Successfully {self.action}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            messages.error(request, f"Something went wrong. Please check the console for more details.")
            if instance_id is not None and instance_id != '':
                return redirect('user_management:user.update', id=URLEncryptionDecryption.dec(int(instance_id)))
            return redirect('user_management:user.create')
        return redirect('user_management:user.index')


class DestroyUserRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                Users.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)

class UserStatusChange(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = Users.objects.get(id = instance_id)
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