from django.contrib import admin



from .models import *
#from .models import Customer

# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    #readonly_fields = ("slug",)
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("price", "on_special",)
    list_display = ("name", "price", "on_special",)

admin.site.register(Item, ItemAdmin)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)






