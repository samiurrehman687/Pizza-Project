# middleware.py
from django.contrib.auth.middleware import LoginRequiredMiddleware
import re
from django.conf import settings
from decouple import config
from account.models import underconstruction
from django.shortcuts import render
import logging

class CustomLoginRequiredMiddleware(LoginRequiredMiddleware):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # media, admin aur registration URLs exempt
        exempt_urls = [
            re.compile(r'^/media/'),
            re.compile(r'^/admin/'),
            re.compile(r'^/register/'),          # registration page
            re.compile(r'^/register/done/'),     # registration done page
            re.compile(r'^/activate/'),          # activation links
        ]

        for pattern in exempt_urls:
            if pattern.match(request.path):
                return None

        return super().process_view(request, view_func, view_args, view_kwargs)



logger = logging.getLogger('account')
class UnderConstMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response
        

    def __call__(self, request):
        if request.user.is_staff:
            return self.get_response(request)
        uc_key = config('under_maintance_key')
        #session set ka 
        
        if 'u' in request.GET and request.GET['u'] == uc_key:
            request.session['Bypass manintance'] = True
            request.session.set_expiry(0)
            logger.info(f"Bypass maintenance session set for IP: {request.META.get('REMOTE_ADDR')}")
            # session get kia
        if request.session.get('Bypass manintance' , False):
            return self.get_response(request)
        try:
            uc = underconstruction.objects.first()
            if uc and uc.is_under_const:
                uc1 = uc.uc_note
                logger.info(f"Under construction page served to IP: {request.META.get('REMOTE_ADDR')}")
                return render(request , 'account/underconstr.html' , {'uc1': uc1})
        except Exception as e:
            logger.error(f"Error in UnderConstMiddleware: {str(e)}")
        return self.get_response(request)