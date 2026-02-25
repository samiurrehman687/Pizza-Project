from django.db import models 
from django.contrib.auth.models import User

# Create your models here 
    
# registor models
    
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    pizza_name = models.CharField('Pizza Name',max_length=255)
    quantity = models.IntegerField('Quantity')
    phone_number = models.CharField('Phone Number',max_length=15)
    status = models.CharField('Status', max_length=20 , default='Pending')

    def __str__(self):
        return self.pizza_name
# Items
class Item(models.Model):
    name = models.CharField('Name',max_length=255)
    picture = models.FileField('Picture', upload_to='items_pictures/')
    in_stock = models.IntegerField('In Stock')
    price = models.IntegerField('Price')

    def __str__(self):
        return self.name
# Customer query 
class CustomerQuery(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField(max_length=2000)

    def __str__(self):
        return self.name
# Site Data Model 
class SiteDataModel(models.Model):
    CHOICE_FIELD = [
        ('home_para' ,'Home Paragraph'),
        ('home_img','Home Image'),
        ('contact', 'Contact No'),
        ('email' , 'Email'),
        ('address', 'Address'),
    ]
    name =  models.CharField(max_length=255, choices=CHOICE_FIELD, unique=True)
    home_imge = models.ImageField(upload_to='home_image/', blank=True)
    text = models.TextField(blank=True, null=True)
    contact_no = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255 , blank= True , null= True)

    def __str__(self):
        return self.name
# if site under construction.....
class underconstruction(models.Model):
    is_under_const = models.BooleanField(default=False)
    uc_note = models.TextField(blank= True , null= True , help_text= 'Note for underconstruciton..')
    uc_duration = models.DateTimeField(blank=True, null=True, help_text='End durations for underconstructioin.....')
    uc_update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Under Construction : {self.is_under_const}' 