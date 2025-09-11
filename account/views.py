from django.shortcuts import render , redirect
from django.views import View
from django.views.generic import ListView , FormView
from account.models import Item , CustomerQuery 
from account.forms import CustomerQueryForm , RegistrationsForm , LoginForm , OrderForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_not_required
from django.utils.decorators import method_decorator
import logging
from django.conf import settings
# email Activation libraries..
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.

logger = logging.getLogger('account')

@method_decorator(login_not_required , name='dispatch')
class PizzaHome(View):
    def get(self, request, *args, **kwargs):
        logger.debug("PizzaHome page accessed by user: %s", request.user)
        return render(request, 'account/home.html')

@method_decorator(login_not_required , name='dispatch')
class PizzaMenu(ListView):
    model = Item
    template_name = 'account/menu.html'
    context_object_name = 'items'

    def get_queryset(self):
        qs = super().get_queryset()
        logger.debug("PizzaMenu accessed, items count: %d", qs.count())
        return qs




@method_decorator(login_not_required , name='dispatch')
class Contact(FormView):
    model = CustomerQuery
    form_class = CustomerQueryForm
    template_name = 'account/contact.html'
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        try:
            form.save()
            logger.info("CustomerQuery form submitted by user: %s", self.request.user)
            messages.success(self.request , 'Form Submitted Please Wait and Check Your Email')
        except Exception as e:
            logger.error("Error saving CustomerQuery form: %s", e)
            messages.error(self.request, "Error submitting form")
        return super().form_valid(form)
    
@method_decorator(login_not_required , name='dispatch')
class Help(View):
    def get(self, request, *args, **kwargs):
        logger.debug("Help page accessed by user: %s", request.user)
        return render(request , 'account/help.html')
@method_decorator(login_not_required , name='dispatch')
class RegistorView(FormView):
    model = User
    form_class = RegistrationsForm
    template_name  = 'account/registor.html'
    success_url = reverse_lazy('registor_done')

    def form_valid(self, form):
        try:
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(form.cleaned_data['password'])
            user.save()
            logger.info("New user registered: %s", user.username)
            messages.success(self.request , 'Form Submitted. Please Activate Your Account')
            self.send_activation_email(user)
        except Exception as e:
            logger.error("Error in user registration: %s", e)
            messages.error(self.request, "Registration failed")
        return super().form_valid(form)
    def send_activation_email(self, user):
        try:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(self.request).domain
            link = f'http://{domain}/activate/{uid}/{token}/'

            send_mail(
                'Activate Your Account',
                f'Click the link to activate your account: {link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            logger.info("Activation email sent to user: %s", user.username)
        except Exception as e:
            logger.error("Error sending activation email to %s: %s", user.username, e)




@method_decorator(login_not_required , name='dispatch')
class ActivateAccountView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            user = None
            logger.error("Activation failed: %s", e)

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            logger.info("User account activated: %s", user.username)
            messages.success(request, 'Your account is activated! You can login now.')
            return redirect('login')
        else:
            logger.warning("Invalid activation attempt")
            messages.error(request, 'Activation link is invalid!')
            return redirect('registor')
        

@method_decorator(login_not_required , name='dispatch')        
class UserLogin(LoginView):
    template_name = 'account/login.html'
    authentication_form=LoginForm
    redirect_authenticated_user = False  # already logged in user redirect
    next_page = 'customer_dash' 
    def form_invalid(self, form):
        logger.warning("Failed login attempt for username: %s", self.request.POST.get('username'))
        return super().form_invalid(form) 
    
class OrderView(FormView):
    template_name = 'account/order.html'
    form_class = OrderForm
    success_url = reverse_lazy('customer_dash')

    login_url = 'login'

    redirect_field_name = 'next'
    
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated or user.is_staff or user.is_superuser:
            logger.warning("Unauthorized access attempt to OrderView by user: %s", user)
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            form.instance.customer = self.request.user
            form.save()
            logger.info("Order placed by user: %s", self.request.user.username)
        except Exception as e:
            logger.error("Error placing order for user %s: %s", self.request.user.username, e)
        return super().form_valid(form)
    