from datetime import timezone
import datetime
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q
from django.utils.html import escape
from pydantic import ValidationError
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
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return OrderProduct.objects.all().order_by('-id')

    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
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


from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages

from .models import OrderProduct
 # Assuming you have a utility for URL encryption/decryption

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.http import JsonResponse

from .models import OrderProduct
  # Assuming you have a utility for URL encryption/decryption
from datetime import datetime

# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import OrderProduct, OrderItem, Product
from django.urls import reverse
from django.contrib import messages
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from datetime import datetime
from .models import OrderProduct, OrderItem, Product

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from datetime import datetime
from .models import OrderProduct, OrderItem, Product

from django.contrib import messages

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from datetime import datetime
from .models import OrderProduct, OrderItem


from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from datetime import datetime
from .models import OrderProduct, OrderItem

# Import necessary modules
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from .models import OrderProduct, OrderItem  # Import your models
 # Import your utility function
 # Assuming you have a Product model

# Import datetime for handling date fields
from datetime import datetime

# Define your view class
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import OrderProduct, OrderItem, Product
 # If you have a utility function for URL encryption/decryption
from django.contrib import messages
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
from datetime import datetime
from .models import OrderProduct, OrderItem, Product


from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages

from .models import OrderProduct, OrderItem

 # Replace 'products' with your actual app name

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from datetime import datetime
from .models import OrderProduct, OrderItem


from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
from datetime import datetime


from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from django.urls import reverse
from django.contrib import messages
from .models import OrderProduct, OrderItem
 # Import your forms

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from django.urls import reverse
from django.contrib import messages

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.db import transaction
 # Import your utility function

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from django.urls import reverse
from django.contrib import messages
# Import your utility function

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from datetime import datetime
from .models import OrderProduct, OrderItem
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
# Assuming this utility is available in your project

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.core.exceptions import ValidationError
from django.contrib import messages


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
            instance = get_object_or_404(OrderProduct, id=id)
            self.context['instance'] = instance
            self.context['order_items'] = instance.orderitem_set.all()

            # Pass selected product IDs to the template
            selected_product_ids = [item.product.id for item in instance.orderitem_set.all()]
            self.context['selected_product_ids'] = selected_product_ids

        products = Product.objects.all()
        self.context['products'] = products

        self.generate_breadcrumbs()
        return render(request, self.template, context=self.context)

    def generate_breadcrumbs(self):
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

            instance.customer_details = request.POST.get('customer_details', None)

            order_date_str = request.POST.get('order_date', None)
            if order_date_str:
                instance.order_date = datetime.strptime(order_date_str, "%Y-%m-%d")

            instance.save()

            # Clear existing order items
            instance.orderitem_set.all().delete()

            total_price = 0

            # Iterate over product data
            for i in range(1, int(request.POST.get('itemCount', 1)) + 1):
                product_id = request.POST.get(f'product_name[{i}]')
                quantity = request.POST.get(f'quantity[{i}]')
                price = request.POST.get(f'price[{i}]')

                print(f"Processing item {i} - Product ID: {product_id}, Quantity: {quantity}, Price: {price}")

                if product_id and quantity and price:
                    if quantity == 'DefaultQuantity' or price == 'DefaultPrice':
                        print("Skipping iteration due to default quantity or price.")
                        continue  # Skip this iteration if quantity or price is set to default

                    try:
                        product = Product.objects.get(id=product_id)
                    except Product.DoesNotExist:
                        print(f"Product with ID {product_id} does not exist.")
                        continue  # Skip this iteration if the product doesn't exist

                    try:
                        order_item = OrderItem.objects.create(
                            product=product,
                            quantity=quantity,
                            price=price,
                            order=instance
                        )
                    except ValidationError as e:
                        print(f"Validation error: {str(e)}")
                        continue  # Skip this iteration if there's a validation error

                    total_price += int(quantity) * float(price)

                    # Print order item information
                    print(f"OrderItem - Product: {product}, Quantity: {quantity}, Price: {price}")
                    print(f"OrderItem saved: {order_item}")

            # Add a final print statement to check if the loop is executed
            print("Loop completed")

            instance.total = total_price
            instance.save()

            messages.success(request, f"Data Successfully " + self.action)

            # Print the received POST data
            print("POST data received:", request.POST)

            return redirect('order:order.index')

        except Exception as e:
            messages.error(request, f"Something went wrong. {str(e)}")
            if instance_id is not None and instance_id != '':
                return redirect('order:order.update', id=URLEncryptionDecryption.dec(int(instance_id)))
            return redirect('order:order.index')
        

    
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
from datetime import datetime



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



from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

from .models import OrderProduct

class OrderPDFView(View):
    template_name = 'order_pdf_template.html'

    def get_context_data(self, order_id):
        order = OrderProduct.objects.get(id=order_id)
        return {'order': order}

    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        template = get_template(self.template_name)
        context = self.get_context_data(order_id)
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="order_{order_id}.pdf"'

        pdf_result = pisa.CreatePDF(html, dest=response)
        if pdf_result.err:
            return HttpResponse('Error generating PDF')

        return response

class OrderPrintDetailsView(View):
    template_name = 'admin/home-page/order/order_print_details.html'

    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')

        # Assuming OrderProduct is your model for orders, and OrderItem is a related model for order items
        try:
            order = OrderProduct.objects.get(id=order_id)
            order_items = order.orderitem_set.all()

            order_details = {
                'order_id': order.id,
                'order_date': order.order_date.strftime('%Y-%m-%d'),
                'status': order.status,  # Assuming status is a field in OrderProduct model
                'order_items': [
                    {'product': item.product.name, 'quantity': item.quantity, 'price': item.price}
                    for item in order_items
                ],
            }

            return render(request, self.template_name, {'order_details': order_details})
        except OrderProduct.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)