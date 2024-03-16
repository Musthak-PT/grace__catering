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
from apps.product.models import Product
from apps.category.models import Category
# Create your views here.
class ProductView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs": []}
        self.template = 'admin/home-page/product/product-list.html'
        self.context['title'] = 'Product'
        self.generateBreadcrumbs()

    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
        self.context['breadcrumbs'].append({"name": "Product", "route": '', 'active': True})      

class LoadProductDatatable(BaseDatatableView):
    model = Product
    order_columns = ['id']

    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return Product.objects.all().order_by('-id')

    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(
            Q(product_name__istartswith=search) |
            Q(category__category_name__istartswith=search)
        )
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'              : escape(item.id),
                'product_name'    : escape(item.product_name),
                'category_name'   : escape(item.category.category_name) if item.category else '',
                'is_active'       : escape(item.is_active),
                'encrypt_id'      : escape(URLEncryptionDecryption.enc(item.id))
            })
        return json_data
class ProductCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs": [], }
        self.action = "Create"
        self.context['title'] = 'Product'
        self.template = 'admin/home-page/product/product-create-or-updatee.html'

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Update"
            self.context['instance'] = get_object_or_404(Product, id=id)

        # Retrieve categories and add them to the context
        categories = Category.objects.filter(is_active=True)
        self.context['categories'] = categories

        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})

        self.context['breadcrumbs'].append({"name": "{} Product".format(self.action), "route": '', 'active': True})

    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('instance_id', None)
        try:
            if instance_id:
                self.action = 'Updated'
                instance = get_object_or_404(Product, id=instance_id)
            else:
                instance = Product()
                self.action = 'Created'

            instance.product_name = request.POST.get('product_name', None)
            category_id = request.POST.get('category', None)
            if category_id:
                category = Category.objects.get(id=category_id)
                instance.category = category
            else:
                instance.category = None

            instance.created_by = request.user
            instance.save()

            messages.success(request, f"Data Successfully " + self.action)
        except Exception as e:
            messages.error(request, f"Something went wrong." + str(e))
            if instance_id is not None and instance_id != '':
                return redirect('product:product.update', id=URLEncryptionDecryption.dec(int(instance_id)))
            return redirect('product:product.create')
        return redirect('product:product.index')

class DestroyProductRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                Product.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)

class ProductStatusChange(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = Product.objects.get(id=instance_id)
            if instance_id:
                if instance.is_active:
                    instance.is_active = False
                else:
                    instance.is_active = True
                instance.save()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as es:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(es)
        return JsonResponse(self.response_format, status=200)