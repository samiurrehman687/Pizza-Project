from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
import logging
Error_403 = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Access Denied</title>
            <style>
            body { display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;
            background: linear-gradient(135deg, #ff4e50, #f9d423); font-family: 'Arial', sans-serif; color: white;
            text-align: center; }
            .access-box { background: rgba(0,0,0,0.6); padding: 40px; border-radius: 15px; box-shadow: 0 0 20px rgba(0,0,0,0.3);
            animation: fadeIn 1s ease-in-out; }
            .access-box h1 { font-size: 3em; margin: 0 0 20px 0; }
            .access-box p { font-size: 1.2em; margin: 0; }
            @keyframes fadeIn { from { opacity: 0; transform: scale(0.8); } to { opacity: 1; transform: scale(1); } }
            </style>
            </head>
            <body>
            <div class="access-box">
            <h1>Access Denied</h1>
            <p>You don’t have permission to view this page.</p>
            </div>
            </body>
            </html>
        """
logger = logging.getLogger('account')
class IsCustomerMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        # User authenticated AND NOT staff/superuser → allowed
        return user.is_authenticated and not user.is_staff and not user.is_superuser

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            logger.warning(f"Forbidden access attempt by user: {self.request.user.username}, IP: {self.request.META.get('REMOTE_ADDR')}")
            return HttpResponseForbidden(Error_403)
        else:
            logger.info(f"Anonymous user tried to access protected view, IP: {self.request.META.get('REMOTE_ADDR')}")
        return redirect('login')
