from django.contrib import admin

# Register your models here.
from order.models import ShopCart, Order, OrderProduct


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'quantity', 'price', 'amount']
    list_filter = ['product', 'user']
    # readonly_fields = ('product', 'rate', 'comment', 'user', 'subject')


class OrderProductline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product', 'width', 'height', 'price', 'quantity', 'amount', 'create_at', 'update_at')
    can_delete = False
    extra = 0
    actions = None


class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'city', 'total', 'status', 'create_at', 'update_at']
    list_filter = ['status']
    readonly_fields = (
        'code', 'user', 'first_name', 'last_name', 'city', 'address', 'phone', 'total', 'create_at', 'update_at')
    can_delete = False
    inlines = [OrderProductline]
    actions = None


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'width', 'height', 'price', 'quantity', 'amount', 'create_at', 'update_at']
    list_filter = ['user']
    actions = None


admin.site.register(ShopCart, ShopCartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)

