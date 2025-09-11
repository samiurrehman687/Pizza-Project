from django.urls import path
from customer import views as v1
urlpatterns = [
    path('customerdash/', v1.CustomerDash.as_view(), name='customer_dash'),
]
