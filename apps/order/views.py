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
from apps.category.models import Category
from apps.order.models import *
# Create your views here.
class OrderView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs": []}
        self.template = 'admin/home-page/order/order-listing.html'
        self.context['categories_title'] = 'Order'
        self.generateBreadcrumbs()

    def get(self, request, *args, **kwargs):
        orders = OrderProduct.objects.all()
        self.context['order'] = orders
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
        self.context['breadcrumbs'].append({"name": "Orders", "route": '', 'active': True})      

class LoadOrderDatatable(BaseDatatableView):
    model = OrderProduct
    order_columns = ['id']

    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        print("Filter Value:", filter_value)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return OrderProduct.objects.all().order_by('-id')

    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        print("Search Value:", search)
        if search:
            qs = qs.filter(
                Q(corder_date__istartswith=search)
            )
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'              : escape(item.id),
                'order_date'      : escape(item.order_date),
                'is_active'       : escape(item.is_active),
                'encrypt_id'      : escape(URLEncryptionDecryption.enc(item.id))
            })
        return json_data