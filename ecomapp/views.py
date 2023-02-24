from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Seller, User, Cart, Review, OrderProduct, \
                    Order, CartProduct, Customer, PaymentMethod, Brand, Category
from django.conf import settings
from django.urls import reverse
from django.http import Http404, HttpResponseBadRequest
from django.db import IntegrityError


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if hasattr(user, 'customer_user'):
                # Redirect to customer account page
                return redirect('home')
            elif hasattr(user, 'seller_user'):
                # Redirect to seller account page
                return redirect('seller_account')
            else:
                # Redirect to default account page
                return redirect('register')
        else:
            error_message = 'Invalid login credentials. Please try again.'
            return render(request, 'ecomapp/login.html', {'error_message': error_message})
    return render(request, 'ecomapp/login.html')



def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        if not request.POST.get('username'):
            error_message = "Please provide a username."
            return render(request, 'ecomapp/register.html', {'error_message': error_message})

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        # **request.POST
        if password != password_confirm:
            error_message = "Passwords don't match. Please try again."
            return render(request, 'ecomapp/register.html', {'error_message': error_message})

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password
        )

        customer = Customer.objects.create(user=user,
                                           first_name=user.first_name,
                                           last_name=user.last_name,
                                           email=user.email)

        Cart.objects.create(owner=customer)

        authenticated_user = authenticate(username=username, password=password)
        login(request, authenticated_user)
        return redirect('home')

    return render(request, 'ecomapp/register.html')


def seller_register(request):
    if request.method == 'POST':
        if not request.POST.get('username'):
            error_message = "Please provide a username."
            return render(request, 'ecomapp/seller_register.html', {'error_message': error_message})

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        if not email:
            error_message = "Please provide an email."
            return render(request, 'ecomapp/seller_register.html', {'error_message': error_message})
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            error_message = "Passwords don't match. Please try again."
            return render(request, 'ecomapp/register.html', {'error_message': error_message})

        try:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
            )

            user.save()

            seller = Seller.objects.create(user=user)
            seller.first_name =user.first_name
            seller.last_name = user.last_name
            seller.email = user.email
            seller.business_name = request.POST.get('business_name')
            seller.phone = request.POST.get('phone')
            seller.address = request.POST.get('address')
            seller.city = request.POST.get('city')
            seller.state = request.POST.get('state')
            seller.zip_code = request.POST.get('zip_code')
            seller.country = request.POST.get('country')

            seller.save()

            cart = Cart()
            cart.id = user.id
            cart.owner = user
            cart.products.set([])

            cart.save()

            authenticated_user = authenticate(username=username, password=password)
            login(request, authenticated_user)
            return redirect('seller_account')

        except IntegrityError:

            error_message = "Email already exists. Please use a different email address."
    return render(request, 'ecomapp/seller_register.html')


def seller_account(request):
    try:
        seller = request.user.seller_user
        products = Product.objects.filter(seller=seller)
    except Seller.DoesNotExist:
        raise Http404("Seller matching query does not exist.")
    context = {'seller': seller, 'products': products}
    return render(request, 'ecomapp/seller_account.html', context)


def edit_seller_profile(request):
    return render(request, 'ecomapp/seller_account.html')


def add_product(request):
    seller = request.user.seller_user
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        image = request.FILES['image']
        description = request.POST['description']
        brand_id = request.POST['brand']
        category_id = request.POST['category']
        quantity = request.POST['quantity']

        brand = Brand.objects.get(id=brand_id)
        category = Category.objects.get(id=category_id)

        Product.objects.create(name=name, price=price, image=image, description=description, brand=brand,
                          category=category, seller=seller, quantity=quantity)

        return redirect('seller_account')

    brands = Brand.objects.all()
    categories = Category.objects.all()
    context = {'brands': brands, 'categories': categories}
    return render(request, 'ecomapp/add_product.html', context)


@login_required
def edit_product(request, product_id):
    seller = request.user.seller_user
    product = get_object_or_404(Product, id=product_id, seller=seller)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        if request.FILES.get('image'):
            product.image = request.FILES['image']
        product.save()
        return redirect('seller_account')

    return render(request, 'ecomapp/edit_product.html', {'product': product})


def delete_product(request, pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    return redirect('seller_account')


def home_view(request):
    products = Product.objects.all().order_by('-id')
    cart_products_count = 0
    if request.user.is_authenticated:
        cart = request.user.customer_user.cart
        cart_products_count = cart.products.count()
    context = {'products': products, 'MEDIA_URL': settings.MEDIA_URL, 'cart_products_count': cart_products_count}
    print(context)
    return render(request, 'ecomapp/home.html', context)


@login_required
def customer_account(request):
    customer = Customer.objects.get(id=request.user.id)
    context = {'customer': customer}
    return render(request, 'ecomapp/customer_account.html', context)


@login_required
def update_account(request):
    customer = request.user.customer_user
    if request.method == 'POST':
        customer.first_name = request.POST.get('first_name')
        customer.last_name = request.POST.get('last_name')
        customer.email = request.POST.get('email')
        customer.phone = request.POST.get('phone')
        customer.address = request.POST.get('address')
        customer.city = request.POST.get('city')
        customer.state = request.POST.get('state')
        customer.zip_code = request.POST.get('zip_code')
        customer.country = request.POST.get('country')
        customer.save()
        return redirect('customer_account')
    return render(request, 'ecomapp/update_account.html', {'customer': customer})


def product_list_view(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'ecomapp/product_list.html', context)


def product_detail_view(request, pk):
    product = Product.objects.get(pk=pk)
    context = {'product': product, 'MEDIA_URL': settings.MEDIA_URL}
    return render(request, 'ecomapp/product_detail.html', context)


@login_required
def order_history_view(request):
    customer = User.objects.get(user=request.user)
    orders = Order.objects.filter(customer=customer)
    context = {'orders': orders}
    return render(request, 'ecomapp/order_history.html', context)


def cart_view(request, pk):
    cart = Cart.objects.get(id=pk)
    products = cart.products.all()
    total_price = 0
    for product in products:
        total_price += product.price
    context = {'products': products, 'total_price': total_price}
    return render(request, 'ecomapp/cart.html', context)


def add_to_cart(request, pk):
    product = Product.objects.get(id=pk)
    cart = Cart.objects.get(owner__user_id=request.user.id)
    print(cart)
    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)
    if created:
        cart_product.quantity = 1
    else:
        cart_product.quantity += 1
    cart_product.save()
    return redirect('home')


def remove_from_cart(request, pk):
    product = Product.objects.get(id=pk)
    cart = Cart.objects.get(id=request.user.customer_user.cart.id)
    cart_product = CartProduct.objects.get(cart=cart, product=product)
    cart_product.delete()
    return redirect('cart', cart.id)


def buy_product(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(id=request.user.id)
    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)
    if created:
        cart_product.quantity = 1
    else:
        cart_product.quantity += 1
    cart_product.save()
    return redirect('cart', cart.id)


def order_check(request):
    if request.method == 'POST':
        # Retrieve customer and cart
        customer = Customer.objects.get(user=request.user.customer_user)
        cart = Cart.objects.get(owner=request.user.)

        # Create order
        order = Order.objects.create(
            customer=request.user,
            payment_method='credit card',
            status="P",  # Set status to "pending"
        )

        # Add products to order
        for product in cart.products.all():
            quantity = cart.cartproduct_set.get(product=product).quantity
            OrderProduct.objects.create(
                order=order,
                product=product,
                quantity=quantity,
            )

        # Update order with shipping details
        order.shipping_address = request.POST.get('address')
        order.shipping_city = request.POST.get('city')
        order.shipping_state = request.POST.get('state')
        order.shipping_zip_code = request.POST.get('zip_code')
        order.shipping_country = request.POST.get('country')
        order.shipping_phone = request.POST.get('phone')
        order.save()

        # Redirect to checkout page
        return render(request, 'ecomapp/checkout.html',
                      {'customer': customer, 'cart': cart, 'order': order})

    else:
        # Retrieve cart and products
        cart = Cart.objects.get(owner=request.user.customer_user)
        products = cart.products.all()

        # Calculate total price of products
        total_price = sum([product.price for product in products])

        return render(request, 'ecomapp/order_check.html',
                      {'cart': cart, 'products': products, 'total_price': total_price,})


def checkout(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        # Retrieve order and update payment details
        order = Order.objects.get(id=order_id)
        order.payment_method = request.POST.get('payment_method')
        order.card_name = request.POST.get('card_name')
        order.card_number = request.POST.get('card_number')
        order.card_exp_month = request.POST.get('card_exp_month')
        order.card_exp_year = request.POST.get('card_exp_year')
        order.card_cvv = request.POST.get('card_cvv')
        order.billing_address = request.POST.get('billing_address')
        order.billing_city = request.POST.get('billing_city')
        order.billing_state = request.POST.get('billing_state')
        order.billing_zip_code = request.POST.get('billing_zip_code')
        order.billing_country = request.POST.get('billing_country')
        order.status = 'C'  # Set status to "completed"
        order.save()

        # Clear the cart
        cart = Cart.objects.get(owner=request.user)
        cart.products.clear()

        # Redirect to order details page
        return redirect('order_detail', order_id=order.id)

    else:
        # Return error if no order id provided
        if not request.GET.get('order_id'):
            return HttpResponseBadRequest("Order id not provided.")

        # Retrieve order and cart
        order_id = request.GET.get('order_id')
        order = Order.objects.get(id=order_id)
        cart = Cart.objects.get(owner=request.user)

        return render(request, 'ecomapp/checkout.html', {'cart': cart, 'order': order})



def order_confirmation(request):
    pass


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {'order': order}
    return render(request, 'ecomapp/order_detail.html', context)


def sort_view(request):
    products = Product.objects.all()
    sort_by = ''
    query = ''
    # if request.method == 'POST' and request.POST.get('query'):
    #     products = products.filter(name__icontains='query')

    if request.method == 'POST':
        sort_by = request.POST.get('sort_by')
        query = request.POST.get('query', '')

    if query:
        products = products.filter(name__icontains=query)

    if sort_by == 'price from low to high':
        products = products.order_by('price')
    elif sort_by == 'price from high to low':
        products = products.order_by('-price')
    elif sort_by == 'by name A-Z':
        products = products.order_by('name')
    elif sort_by == 'by name Z-A':
        products = products.order_by('-name')

    if query:
        products = products.filter(name__icontains=query)

    context = {
        'products': products,
        'MEDIA_URL': settings.MEDIA_URL,
        'sort_by': sort_by or '',  # set default to empty string
        'query': query
    }
    return render(request, 'ecomapp/home.html', context)










