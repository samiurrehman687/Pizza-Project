from django.shortcuts import render
from django.views.generic import TemplateView
from account.mixins import IsCustomerMixin
from account.models import Order
# Create your views here.

class CustomerDash(IsCustomerMixin,TemplateView):
    template_name = 'customer/customer_dashboard.html' 
    login_url = '/login/'  # exact path
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Sirf current user ke orders
        context['orders'] = Order.objects.filter(customer=self.request.user)
        return context
