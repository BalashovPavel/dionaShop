from django.contrib import admin

# Register your models here.
from order.models import ShopCart


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'quantity', 'price', 'amount']
    list_filter = ['product', 'user']
    # readonly_fields = ('product', 'rate', 'comment', 'user', 'subject')


admin.site.register(ShopCart, ShopCartAdmin)
