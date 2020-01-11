from django.contrib import admin
from .models import User, Farm, FarmProduct, ShoppingCart, ShoppingCartItem, Review, OrderedItem, Order

# Register your models here.
admin.site.register(User)
admin.site.register(Farm)
admin.site.register(FarmProduct)
admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItem)
admin.site.register(Order)
admin.site.register(OrderedItem)
admin.site.register(Review)
