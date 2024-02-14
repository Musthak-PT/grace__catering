from django.shortcuts import render
from django.utils.html import escape
from .models import SubscribersList
from django.views import View
from django.urls import reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q
# Create your views here.


class SubscriptionlistView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/home-page/subscription/subscription_list.html'
        self.context['title'] = 'Subscription'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Subscription", "route" : '','active' : True})
        

class LoadSubscriptionDatatable(BaseDatatableView):
    order_columns = ['id']
    
    def get_initial_queryset(self):
        model = SubscribersList.objects.all()
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return model.objects.filter(is_active=False).order_by('-id')
        else:
            return model.order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(subscribers_email__istartswith=search))
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'              : escape(item.id),
                'email'           : escape(item.subscribers_email),
                'date_time'       : escape(item.created_date.strftime("%d-%m-%Y %H:%M:%S")),
            })
        return json_data