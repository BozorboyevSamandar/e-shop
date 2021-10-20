from django.contrib import admin
from order.models import Order, Shopcart, OrderProduct


class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'total', 'status']


admin.site.register(Shopcart)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
