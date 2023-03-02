from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from .views import (
    login_view,
    logout_view,
    register_view,
    product_list_view,
    product_detail_view,
    home_view,
    cart_view,
    buy_product,
    add_to_cart,
    remove_from_cart,
    customer_account,
    update_account,
    buy_product,
    checkout,
    seller_register,
    seller_account,
    edit_seller_profile,
    add_product,
    edit_product,
    delete_product,
    order_detail,
    order_check,
    order_history,
    seller_details,
    write_review,
    add_payment_method,
    remove_image
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('product_list/', product_list_view, name='product_list'),
    path('product_detail/<int:pk>/', product_detail_view, name='product_detail'),
    path('', home_view, name='home'),
    path('cart/<int:pk>/', cart_view, name='cart'),
    path('add_to_cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('buy_product/<int:pk>/', buy_product, name='buy_product'),
    path('remove_from_cart/<int:pk>/', remove_from_cart, name='remove_from_cart'),
    path('customer_account/', customer_account, name='customer_account'),
    path('update_account/', update_account, name='update_account'),
    path('checkout/<int:order_id>', checkout, name='checkout'),
    path('buy/<int:product_id>/', buy_product, name='buy_product'),
    path('seller_register/', seller_register, name='seller_register'),
    path('seller_account/', seller_account, name='seller_account'),
    path('edit_seller_profile/', edit_seller_profile, name='edit_seller_profile'),
    path('add_product/', add_product, name='add_product'),
    path('edit_product/<int:product_id>', edit_product, name='edit_product'),
    path('delete_product/<int:product_id>', delete_product, name='delete_product'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
    path('order_check', order_check, name='order_check'),
    path('order_history/', order_history, name='order_history'),
    path('seller_details/<int:seller_id>/', seller_details, name='seller_details'),
    path('write_review/<int:product_id>/', write_review, name='write_review'),
    path('add_payment_method/', add_payment_method, name='add_payment_method'),
    path('remove_image/<int:product_id>/<int:image_id>/', remove_image, name='remove_image'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
