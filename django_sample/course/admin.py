from django.contrib import admin
from .models import Course, Order, OrderItem, Cart, CartItem

admin.site.register(Course)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)