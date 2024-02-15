from django.shortcuts import render
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
from apps.users.models import Users

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
        datefilter = self.request.POST.get('columns[4][search][value]', None)

        queryset = self.model.objects.all()

        # print('datefilter :: ', datefilter)

        # if datefilter is not None and datefilter != '':
        #     filter_start_date, filter_end_date = datefilter.split(' - ')
        #     if filter_start_date:
        #         start_date = datetime.strptime(filter_start_date, '%d/%m/%Y').date()
        #         queryset = queryset.filter(Q(date_joined__gte=start_date))

        #     if filter_end_date:
        #         end_date = datetime.strptime(filter_end_date, '%d/%m/%Y').date()
        #         queryset = queryset.filter(Q(date_joined__lte=end_date + timedelta(days=1)))

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
                'image'         : escape(self.request.build_absolute_uri(item.image.url)),
                'first_name'    : escape(item.first_name),
                'last_name'     : escape(item.last_name),
                'email'         : escape(item.email),
                'phone'         : escape(item.phone),
                'date_joined'   : escape(item.date_joined.strftime("%d-%m-%Y")),
                'is_active'     : escape(item.is_active),
                'encrypt_id'    : escape(URLEncryptionDecryption.enc(item.id)),

            })
        return json_data