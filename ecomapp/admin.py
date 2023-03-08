from django.contrib import admin
from .models import Seller, Brand, Category, Product, Cart, Review, CartProduct, Customer, PaymentMethod, OrderProduct, Order

# admin.site.register(Customer)
# admin.site.register(PaymentMethod)
# admin.site.register(Seller)
# admin.site.register(Brand)
# admin.site.register(Category)
# admin.site.register(Product)
# admin.site.register(Cart)
# admin.site.register(CartProduct)
# admin.site.register(Review)
# admin.site.register(OrderProduct)
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'zip_code', 'country')

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'name', 'card_number', 'expiry_month', 'expiry_year', 'cvv', 'billing_address', 'billing_city', 'billing_state', 'billing_zip_code', 'billing_country', 'is_active')

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'avg_rate', 'business_name', 'first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'zip_code', 'country')

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'image', 'description', 'brand', 'category', 'seller', 'quantity', 'avg_rate')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner',)

@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'rating', 'customer', 'product', 'date_added')

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date_placed', 'status', 'payment_type', 'shipping_address', 'shipping_city', 'phone')


