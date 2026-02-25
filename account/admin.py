from django.contrib import admin
from account.models import Order, Item , CustomerQuery , underconstruction , SiteDataModel
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'pizza_name',
        'quantity',
        'phone_number',
    )
    list_filter = ('customer',)


@admin.register(Item)
class ItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'picture', 'in_stock', 'price')
    search_fields = ('name',)
    list_filter = ('name',)

@admin.register(CustomerQuery)
class ContactQueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'subject', 'message')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('name',)




@admin.register(underconstruction)
class underconstructionAdmin(admin.ModelAdmin):
    list_display = ('is_under_const', 'uc_note', 'uc_duration', 'uc_update_at')
    fields = ('uc_note', 'uc_duration','is_under_const')

@admin.register(SiteDataModel)
class SiteModelAdmin(admin.ModelAdmin):
    list_display = ('name' , 'text')
    search_fields = ('name',)