from django.contrib import admin
from .models import Seller, Brand, Category, Product, Cart, Review, CartProduct, Customer, PaymentMethod

admin.site.register(Customer)
admin.site.register(PaymentMethod)
admin.site.register(Seller)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Review)
