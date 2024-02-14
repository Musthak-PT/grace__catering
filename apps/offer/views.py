from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse
from django.utils.html import escape
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from solo_core.helpers.signer import URLEncryptionDecryption
from django.http import JsonResponse
from .models import PropertyOffer
from django.contrib import messages
from apps.property_management.models import PropertyManagement, PropertyManagementHotelRoom
# Create your views here.

# Start Offer Management
class OfferManagementView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/offer_management/offer-management-list.html'  
        self.context['title'] = 'Offer Management'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Offer Management", "route" : '','active' : True})


class LoadOfferManagementDatatable(BaseDatatableView):
    model = PropertyOffer
    order_columns = ['id', 'room_property', 'start_date','end_date','offer_percentage'] 
    
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return PropertyOffer.objects.filter().order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(room_property__property_management__name__istartswith=search) & Q(title__istartswith=search) & Q(description__istartswith=search))
        return qs
    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'              : escape(item.id),
                'property_name'   : escape(item.room_property.property_management.name),
                'room_name'       : escape(item.room_property.hotel_room.room_type.name),
                'title'           : escape(item.title),
                'start_date'      : escape(item.start_date.strftime("%d-%m-%Y")),
                'end_date'        : escape(item.end_date.strftime("%d-%m-%Y")),
                'percentage'      : escape(item.offer_percentage),
                'is_active'       : escape(item.is_active),
                'encrypt_id'      : escape(URLEncryptionDecryption.enc(item.id)),
            })
        return json_data


class OfferManagementCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.context = {"breadcrumbs": []}
        self.context['title'] = 'Offer Management'
        self.action = "Create"
        self.template = 'admin/home-page/offer_management/create-or-update-offer-management.html'

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        self.context['property_query_set'] = PropertyManagement.objects.all()
        if id:
            self.action = "Update "
            offer_management_obj = get_object_or_404(PropertyOffer, id=id)
            self.context['offer_management_obj']    = offer_management_obj
            self.context['property_room_query_set'] = PropertyManagementHotelRoom.objects.filter(property_management_id=offer_management_obj.room_property.property_management.id)
            
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
        self.context['breadcrumbs'].append(
            {"name": "Offer Management ", "route": reverse('offer_management:offer_management.view.index'), 'active': False})
        self.context['breadcrumbs'].append({"name": "{} Offer Management".format(self.action), "route": '', 'active': True})

    def post(self, request, *args, **kwargs):
        offer_management_id = request.POST.get('offer_management_id', None)
        try:
            if offer_management_id:
                self.action = 'Updated'
                offer_management_obj         = get_object_or_404(PropertyOffer, id=offer_management_id)
            else:
                offer_management_obj         = PropertyOffer()
            offer_management_obj.room_property_id    = PropertyManagementHotelRoom.objects.filter(id=request.POST.get('room_name')).first().id
            offer_management_obj.start_date          = request.POST.get('start_date')
            offer_management_obj.end_date            = request.POST.get('end_date')
            offer_management_obj.offer_percentage    = request.POST.get('percentage')
            offer_management_obj.title               = request.POST.get('title')
            offer_management_obj.description         = request.POST.get('description')
            
            if request.FILES.__len__() != 0:
                if request.POST.get('offer_image', None) is None:
                    offer_management_obj.image = request.FILES.get('offer_image')
            offer_management_obj.save()
            
            messages.success(request, f"Data Successfully "+ self.action)
        
        except Exception as e:
            messages.error(request, f"Something went wrong."+str(e))
            if offer_management_id is not None:
                return redirect('offer_management:offer_management.update', id=URLEncryptionDecryption.dec(int(offer_management_id)))
            return redirect('offer_management:offer_management.create')
        return redirect('offer_management:offer_management.view.index')


class GetRoomListView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": "", "data" : []}
        
    def post(self, request, *args, **kwargs):
        try:
            property_id = request.POST.get('pk', None)
            if property_id:
                rooms = PropertyManagementHotelRoom.objects.filter(property_management_id=property_id)
                json_data = []
                for item in rooms:
                    json_data.append({
                        'id' : escape(item.id), 
                        'name' : escape(item.hotel_room.room_type.name), 
                    })
                    
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
                self.response_format['data'] = json_data
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)
    

@method_decorator(login_required, name='dispatch')
class DestroyOfferManagementRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                PropertyOffer.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)


class OfferManagementStatusChange(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = PropertyOffer.objects.get(id = instance_id)
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

# End