from django.contrib import admin

from .models import *

admin.site.site_header = "Douka Langou"
admin.site.site_title = "Gestionnaire du site"
admin.site.index_title="Administration du site"

class AddressAdmin(admin.ModelAdmin):
    list_display=[
        'address_line_1',
        'address_line_2',
        'city',
        'zip_code',
        'address_type',
    ]
class ProductAdmin(admin.ModelAdmin):
    list_display=[
        'title',
        'price',
    ]    
    
    search_fields=('title',)
    list_editable=('price',)


admin.site.register(Product,ProductAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(ColourVariation)
admin.site.register(SizeVariation)




