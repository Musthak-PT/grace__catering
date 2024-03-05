import json
import logging
import uuid
from apps.home.functions import ConvertBase64File
from solo_core import settings
from solo_core.helpers.module_helper import imageDeletion
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
from solo_core.helpers.signer import URLEncryptionDecryption
import requests
from urllib.parse import urlparse
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
logger = logging.getLogger(__name__)
from apps.users.models import Users
from apps.category.models import Category
from apps.product.models import Product

class HomeView(View):
    def __init__(self):
        self.context = {}
        self.context['title'] = 'Dashboard'

    def get(self, request, *args, **kwargs):
        
        # if request.user.is_superuser:
        #     user_queryset = Users.objects.filter(Q(user_type='2') & Q(is_active=True))
        #     room_booking_obj = RoomBookedCustomerDetails.objects.all()
        #     email_set = set()
        #     user_queryset_list = []
        #     for user in user_queryset:
        #         if user.email not in email_set:
        #             user_queryset_list.append({'full_name': user.full_name})
        #             email_set.add(user.email)
        #     for booking in room_booking_obj:
        #         if booking.email_address not in email_set:
        #             user_queryset_list.append({'full_name': booking.full_name})
        #             email_set.add(booking.email_address)
        #     self.context['total_customers'] = len(user_queryset_list)
        # else:
        #     property_management_obj = PropertyManagementHotelRoom.objects.filter(property_management__assigned_to=request.user).values_list('hotel_room', flat=True)
        #     booking_obj = HotelRoomBookingBookingPrice.objects.filter(booked_room__room_id__in=property_management_obj).values_list('booked_room', flat=True)
        #     user_list_obj = HotelRoomBookingCustomerDetails.objects.filter(booked_room__id__in=booking_obj).values_list('guest_details', flat=True)
        #     result_list = len(set(user_list_obj))
        #     self.context['total_customers'] = result_list if result_list else 0


        # if request.user.is_superuser:
        #     properties = PropertyManagement.objects.all()
        # else:
        #     properties = PropertyManagement.objects.filter(assigned_to=request.user)
        # total_properties = properties.count()
        # self.context['total_properties'] = total_properties

        
        
        # contactus = ContactUs.objects.filter(enquiry_type='1')
        # if contactus:
        #     self.context['total_contacted']=contactus.filter(is_contacted=True).count()
        #     self.context['total_not_contacted']=contactus.filter(is_contacted=False).count()

        # else:
        #     self.context['total_contacted']= 0
        #     self.context['total_not_contacted']= 0
        
        # partner = ContactUs.objects.filter(enquiry_type='2')
        # if partner:
        #     self.context['total_contacted_partner']=partner.filter(is_contacted=True).count()
        #     self.context['total_not_contacted_partner']=partner.filter(is_contacted=False).count()

        # else:
        #     self.context['total_contacted_partner']= 0
        #     self.context['total_not_contacted_partner']= 0
        
        
        
        if request.user.is_superuser:
            categories = Category.objects.all()
        else:
            categories = Category.objects.all()
        total_categories = categories.count()
        self.context['total_categories'] = total_categories

        if request.user.is_superuser:
            products = Product.objects.all()
        else:
            products = Product.objects.all()
        total_products = products.count()
        self.context['total_products'] = total_products
                
             
                


            
            
        return render(request, "admin/home/dashboard.html", self.context)

