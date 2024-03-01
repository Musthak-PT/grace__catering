from datetime import timezone
import datetime
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
    

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.urls import reverse
from .models import OrderProduct


from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.urls import reverse
from .models import OrderProduct


from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from django.contrib import messages
from .models import OrderProduct, Product


class OrderCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs": []}
        self.action = "Create"
        self.context['title'] = 'Order'
        self.template = 'admin/home-page/order/order-create-or-update.html'

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Update"
            self.context['instance'] = get_object_or_404(OrderProduct, id=id)

        # Retrieve products and add them to the context
        products = Product.objects.all()
        self.context['products'] = products

        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
        self.context['breadcrumbs'].append({"name": "{} Order".format(self.action), "route": '', 'active': True})


    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.get('instance_id', None)
            if instance_id:
                self.action = 'Updated'
                instance = get_object_or_404(OrderProduct, id=instance_id)
            else:
                instance = OrderProduct()
                self.action = 'Created'

            # Save the instance to get an ID before adding products
            instance.save()

            # Assuming 'product_name', 'quantity', 'price' are multiple inputs with the same name
            # Inside your OrderCreateOrUpdateView
            product_names = request.POST.getlist('product_name[]')
            quantities = request.POST.getlist('quantity[]')
            prices = request.POST.getlist('price[]')

            # Clear existing product_name entries if it is not None
            if instance.product_name is not None:
                instance.product_name.clear()

            # Add the new products
            for product_name, quantity, price in zip(product_names, quantities, prices):
                product = Product.objects.get(id=product_name)
                instance.product_name.add(product, through_defaults={'quantity': quantity, 'price': price})

            instance.customer_details = request.POST.get('customer_details', None)
            instance.order_date = request.POST.get('order_date', None)

            # Format order_date using strftime
            
            instance.save()

            messages.success(request, f"Data Successfully " + self.action)

        except Exception as e:
            messages.error(request, f"Something went wrong. {str(e)}")
            if instance_id is not None and instance_id != '':
                return redirect('order:order.update', id=URLEncryptionDecryption.dec(int(instance_id)))
            return redirect('order:order.create')
        return redirect('order:order.index')

    

from django.views import View
from django.contrib import messages
from django.urls import reverse
from .models import OrderProduct



class DestroyorderRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                OrderProduct.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)

class OrderStatusChange(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = OrderProduct.objects.get(id=instance_id)
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