from django.contrib import admin
from .models import Seller, Brand, Category, Product, Cart, Review

admin.site.register(Seller)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Review)
