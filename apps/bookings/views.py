import json
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q
from django.utils.html import escape
from django.http import JsonResponse
from apps.bookings.api.booking_email import manual_booking_confirmed_mail_send_customer
from apps.offer.models import PropertyOffer
from solo_core.helpers.signer import URLEncryptionDecryption
from .models import BookingPrice, HotelRoomBookingBookingPrice, HotelRoomBookingCustomerDetails, RoomBookedCustomerDetails, HotelRoomBooking
from apps.property_management.models import HotelRoom, PropertyManagement, PropertyManagementHotelRoom
from django.contrib import messages
from uuid import uuid4
import uuid, os
from solo_core.helpers.helper import ConvertBase64File
from datetime import datetime
from urllib.parse import urlparse
from django.utils import timezone
from apps.bookings.url_base64_convert import url_to_base64
# Create your views here.

# Room Booking 

class ManualRoomBookingView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/bookings/manual-booking/manual-room-booking-list.html'
        self.context['title'] = 'Manual Room Booking'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Manual Room Booking", "route" : '','active' : True})


class LoadRoomBookingDatatable(BaseDatatableView):
    
    order_columns = ['id', 'full_name', 'email_address', 'mobile_number'] 
    
    def get_initial_queryset(self):
        # import pdb;pdb.set_trace()
        model                   = BookingPrice.objects.filter(Q(is_enquiry=False))
        if self.request.user.is_superuser == False:
            property_management_obj = PropertyManagementHotelRoom.objects.filter(property_management__assigned_to=self.request.user).values_list('hotel_room', flat=True)
            booking_obj             = HotelRoomBookingBookingPrice.objects.filter(booked_room__room_id__in=property_management_obj).values_list('booked_price', flat=True)
            model                   = BookingPrice.objects.filter(Q(is_enquiry=False) & Q(id__in=list(set(booking_obj)))).order_by('-id')
        
        
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return model.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return model.filter(is_active=False).order_by('-id')
        else:
            return model.filter().order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(customer_details__full_name__istartswith=search)|Q(customer_details__email_address__istartswith=search))
        return qs

    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:     
            json_data.append({
                'id'                 : escape(item.id),
                'customer_name'      : escape(item.customer_details.full_name),
                'customer_email'     : escape(item.customer_details.email_address),
                'phone'              : escape(item.customer_details.mobile_number),
                'total_booked_price' : escape(item.total_booked_price),
                'payment_status'     : escape(item.is_paid),
                'date_time'          : escape(item.created_date.strftime("%d-%m-%Y %H:%M:%S")),
                'encrypt_id'         : escape(URLEncryptionDecryption.enc(item.id)),
            })
        return json_data
    
class RoomBookingPaymentStatusChange(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = BookingPrice.objects.get(id = instance_id)
            if instance_id:
                if not instance.is_paid:
                    instance.is_paid = True
                else:
                    instance.is_paid = False
                instance.save()
                self.response_format['status_code']=200
                self.response_format['message']= 'Success'
                
        except Exception as es:
            self.response_format['message']='error'
            self.response_format['error'] = str(es)
        return JsonResponse(self.response_format, status=200)

class ManualRoomBookingCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.context = {"breadcrumbs": []}
        self.context['title'] = 'Room Bookings'
        self.action = "Created"
        self.template = 'admin/home-page/bookings/manual-booking/create-or-update-manual-room-booking.html'

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        self.context['uuid'] = uuid.uuid4()
        if id:
            self.action = "Updated"
            booked_price_obj       = get_object_or_404(BookingPrice, id=id)
            # hotel_room_booking_obj = HotelRoomBookingBookingPrice.objects.filter(booked_price=booked_price_obj)
            hotel_rooms_obj        = HotelRoomBookingBookingPrice.objects.filter(booked_price_id=id)
            
            result_list = []
            coustomer_loop_count = 0
            for item in hotel_rooms_obj:
                room_objects = HotelRoomBooking.objects.filter(id=item.booked_room.id)
                for room in room_objects:
                    property_obj = PropertyManagementHotelRoom.objects.filter(hotel_room=room.room_id)
                    
                    row_item = {'room_sl_no':room.room_sl_no, 'room_queryset':property_obj, 'property_name': property_obj.first().property_management, 'room_name': room.room_id, 'no_of_adults': room.adults, 'no_of_childrens': room.childrens}
                    customer_obj = HotelRoomBookingCustomerDetails.objects.filter(booked_room=room)
                    if customer_obj:
                        
                        customer_list = []
                        for customer in customer_obj:
                            url_base64 = url_to_base64(request.build_absolute_uri(customer.guest_details.document.url))
                            customer_list.append({'coustomer_loop_count': coustomer_loop_count,'customer_details_id':customer.guest_details.id, 'full_name': customer.guest_details.full_name, 'email_address': customer.guest_details.email_address, 'mobile_number': customer.guest_details.mobile_number, 'dob':customer.guest_details.dob, 'document': url_base64})
                            
                        row_item['customer_details'] = customer_list
                            
                    else:
                        row_item['customer_details'] = [{'coustomer_loop_count': coustomer_loop_count,'customer_details_id':'', 'full_name': '', 'email_address': '', 'mobile_number': '', 'dob':'', 'document': ''}]
                    coustomer_loop_count +=1
                    
                    
                result_list.append(row_item)
                
                
                
            self.context['booked_hotel_rooms_obj']  = hotel_rooms_obj.first()
            self.context['booked_price_obj']        = booked_price_obj
            self.context['booked_room_list']        = result_list
        if self.request.user.is_superuser:
            property_m_obj = PropertyManagement.objects.all()
        else:
            property_m_obj = PropertyManagement.objects.filter(assigned_to=self.request.user)
            
        self.context['properties_queryset']         = property_m_obj
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
        self.context['breadcrumbs'].append(
            {"name": "Manual Booking", "route": reverse('bookings:manual_booking.index'), 'active': False})
        self.context['breadcrumbs'].append({"name": "{} Manual Booking".format(self.action), "route": '', 'active': True})
        
        
    def post(self, request, *args, **kwargs):
        manual_booking_id    = request.POST.get('manual_booking_id', None)
        booked_room_details_and_document = request.POST.get('booked_room_details_and_document', None)
        
        try:
            
            
            booked_customer_obj         = BookingPrice()
            check_out = datetime.strptime(request.POST.get('checkout'), '%Y-%m-%d')
            check_in  = datetime.strptime(request.POST.get('check_in'), '%Y-%m-%d')
            adults    = request.POST.get('adults')
            childrens = request.POST.get('childrens')
            guest_owner_email = request.POST.get('email')
            guest_obj = RoomBookedCustomerDetails(full_name       = request.POST.get('name'),
                                                  email_address   = request.POST.get('email'),
                                                  mobile_number   = request.POST.get('phone'),
                                                  guest_address   = request.POST.get('address'),
                                                  is_enquired     = True
                                                  )
            guest_obj.save()
            
            booked_room_obj = json.loads(booked_room_details_and_document)
            
            total_room_price_list = []
            room_obj_list = []
            for item in booked_room_obj:
                
                # room_row = HotelRoom.objects.filter(id=item['room_name'])
                room_row = PropertyManagementHotelRoom.objects.filter(id=item['room_name']).first()
                room_row = HotelRoom.objects.filter(id=room_row.hotel_room.id).first()
                
                room_obj = HotelRoomBooking(room_sl_no = item["room_sl_no"], 
                                            room_id   = room_row,
                                            # quantity  = item['no_of_rooms'],
                                            check_in  = check_in,
                                            check_out = check_out,
                                            adults    = item['no_of_adults'],
                                            childrens = item['no_of_childrens']
                                            )

                offer_obj = PropertyOffer.objects.filter(Q(room_property__hotel_room=room_row) & Q(start_date__lte=check_in) & Q(end_date__gte=check_out)).first()
                num_days = (check_out - check_in).days  if (check_out - check_in).days > 0 else 1
                
                actual_price = int(room_row.price) * num_days
                if offer_obj:
                    actual_price = int((actual_price - (actual_price * (int(offer_obj.offer_percentage) / 100))))
                total_room_price_list.append(actual_price)
                room_obj.booked_room_price = str(actual_price)
                room_obj.save()
                room_obj_list.append(room_obj.id)
                final_result_list = []
                for customer in item["customer_details"]:
                    customer_obj = RoomBookedCustomerDetails(full_name = customer['full_name'],
                                                    email_address    = customer['email'],
                                                    mobile_number    = customer['phone_number'],
                                                    dob              = customer['dob'],                    
                                                    )
                    customer_obj.save()
                    file_string = customer['documents']
                    if file_string:
                        extension           = ConvertBase64File().base64_file_extension(file_string)
                        
                        output_schema_xsd   = ConvertBase64File().base64_to_file(file_string)
                        unique_filename     = f'{uuid4()}.{extension}'
                        customer_obj.document.save(unique_filename, output_schema_xsd, save = True)
                        customer_obj.save()
                        customer_obj = HotelRoomBookingCustomerDetails.objects.create(
                                                        booked_room        = room_obj,
                                                        guest_details      = customer_obj               
                                                        )
                        final_result_list.append(customer_obj)

            booking_price = BookingPrice.objects.create(
                total_booked_price=sum(total_room_price_list),
                is_paid=False,
                is_enquiry=False,
                customer_details = guest_obj
            )

            HotelRoomBookingBookingPrice.objects.bulk_create([
                HotelRoomBookingBookingPrice(booked_room_id=room, booked_price=booking_price)
                for room in room_obj_list
            ])
            
            
            
            if manual_booking_id:
                self.action = 'Updated'
                booked_customer_obj         = get_object_or_404(BookingPrice, id=manual_booking_id)
                book_price__update_obj      = HotelRoomBookingBookingPrice.objects.filter(booked_price=booked_customer_obj)
                
                
                for i in book_price__update_obj:
                    hotel_update_obj = HotelRoomBooking.objects.filter(id=i.booked_room.id)
                    i.delete()
                    for j in hotel_update_obj:
                        customer_obj = HotelRoomBookingCustomerDetails.objects.filter(booked_room=j)
                        j.delete()
                        for k in customer_obj:
                            RoomBookedCustomerDetails.objects.filter(id=k.guest_details.id).delete()
                            k.delete()
                booked_customer_obj.delete()
            # if manual_booking_id:
            manual_booking_confirmed_mail_send_customer(request, guest_obj, final_result_list, check_in, check_out,
                                        guest_owner_email)
            messages.success(request, f"Data Successfully "+ self.action)
            
        except Exception as e:
            messages.error(request, f"Something went wrong."+str(e))
            if manual_booking_id is not None:
                return redirect('bookings:manual_booking.update', id=URLEncryptionDecryption.dec(int(manual_booking_id)))
            return redirect('bookings:manual_booking.create')
        return redirect('bookings:manual_booking.index')

# End 

class GetBookingCustomerImages(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": "", "data" : []}
    def post(self, request, *args, **kwargs):
        try:
            property_id = request.POST.get('pk')
            if property_id:
                property_images = RoomBookedCustomerDetails.objects.filter(id=property_id)
                json_data = []
                for item in property_images:
                    json_data.append({
                        'id'         : escape(item.id), 
                        'image'      : escape(request.build_absolute_uri(item.document.url)), 
                        'image_name' : escape(os.path.basename(urlparse(request.build_absolute_uri(item.document)).path)), 
                        'size'       : escape(item.document.size), 
                    })

                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
                self.response_format['data'] = json_data
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)
    

# Enquiry Booking
    
class EnquiryListBookingView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/bookings/booking_enquiry/enquiry-room-booking-list.html'
        self.context['title'] = 'Enquiry Booking'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Enquiry Booking", "route" : '','active' : True})


class LoadShowEnquiryBookingDatatable(BaseDatatableView):
    order_columns = ['id', 'full_name', 'email_address', 'mobile_number'] 
    
    def get_initial_queryset(self):
        # import pdb;pdb.set_trace()
        model                   = BookingPrice.objects.filter(Q(is_enquiry=True))
        if self.request.user.is_superuser == False:
            property_management_obj = PropertyManagementHotelRoom.objects.filter(property_management__assigned_to=self.request.user).values_list('hotel_room', flat=True)
            booking_obj             = HotelRoomBookingBookingPrice.objects.filter(booked_room__room_id__in=property_management_obj).values_list('booked_price', flat=True)
            model                   = BookingPrice.objects.filter(Q(is_enquiry=True) & Q(id__in=list(set(booking_obj))))
        
        
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return model.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return model.filter(is_active=False).order_by('-id')
        else:
            return model.filter().order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(customer_details__full_name__istartswith=search)|Q(customer_details__email_address__istartswith=search))
        return qs

    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:     
            json_data.append({
                'id'                 : escape(item.id),
                'customer_name'      : escape(item.customer_details.full_name),
                'customer_email'     : escape(item.customer_details.email_address),
                'phone'              : escape(item.customer_details.mobile_number),
                'total_booked_price' : escape(item.total_booked_price),
                'payment_status'     : escape(item.is_paid),
                'date_time'          : escape(item.created_date.strftime("%d-%m-%Y %H:%M:%S")),
                'encrypt_id'         : escape(URLEncryptionDecryption.enc(item.id)),
            })
        return json_data


   