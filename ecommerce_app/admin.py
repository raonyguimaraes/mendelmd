from django.contrib import admin
from .models import Product, Order, CartItem, LineItem

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_type', 'user', 'date', 'total_cost', 'paid', 'payment_status']

    def get_total_cost(self, obj):
        return obj.total_cost()
    get_total_cost.short_description = 'Total Cost'


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'quantity', 'product']


class LineItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'quantity', 'date_added', 'order']


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(CartItem, OrderItemAdmin)
admin.site.register(LineItem, LineItemAdmin)