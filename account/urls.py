from django.urls import path
from account import views as v1
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', v1.PizzaHome.as_view(), name='home'),
    path('menu/', v1.PizzaMenu.as_view(), name='menu'),
    path("contact/", v1.Contact.as_view(), name="contact"),
    path("help/", v1.Help.as_view(), name="help"),
    path("regdone/", TemplateView.as_view(template_name='account/registor_done.html'), name="registor_done"),
    path("registor/", v1.RegistorView.as_view(), name="registor"),
    path('activate/<uidb64>/<token>/', v1.ActivateAccountView.as_view(), name='activate'),
    path('login/',v1.UserLogin.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path("order/", v1.OrderView.as_view(), name="order"),



    # Password reset
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name="password_reset_complete"),
    
]

