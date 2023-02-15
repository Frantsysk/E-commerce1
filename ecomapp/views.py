from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Seller, User, Cart, Review, Order, CartProduct, Customer, PaymentMethod
from django.conf import settings


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid login credentials. Please try again.'
            return render(request, 'ecomapp/login.html', {'error_message': error_message})
    return render(request, 'ecomapp/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

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
        user.save()

        cart = Cart()
        cart.id = user.id
        cart.owner = user
        cart.products.set([])

        cart.save()

        authenticated_user = authenticate(username=username, password=password)
        login(request, authenticated_user)
        return redirect('home')

    return render(request, 'ecomapp/register.html')


def home_view(request):
    products = Product.objects.all()
    if request.method == 'POST':
        query = request.POST.get('query')
        products = products.filter(name__icontains=query)
    context = {'products': products, 'MEDIA_URL': settings.MEDIA_URL}
    return render(request, 'ecomapp/home.html', context)


@login_required
def seller_account_view(request):
    seller = Seller.objects.get(user=request.user)
    products = Product.objects.filter(seller=seller)
    context = {'seller': seller, 'products': products}
    return render(request, 'ecomapp/seller_account.html', context)


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
    cart = Cart.objects.get(id=request.user.id)
    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)
    if created:
        cart_product.quantity = 1
    else:
        cart_product.quantity += 1
    cart_product.save()
    return redirect('home')


def remove_from_cart(request, pk):
    product = Product.objects.get(id=pk)
    cart = Cart.objects.get(id=request.user.id)
    cart_product = CartProduct.objects.get(cart=cart, product=product)
    cart_product.delete()
    return redirect('cart', cart.id)

def buy_product(request, product_id):
    return redirect('home')


def sort_view(request):
    products = Product.objects.all()
    if request.method == 'POST':
        sort_by = request.POST.get('sort_by')
        if sort_by == 'price from low to high':
            products = products.order_by('price')
        elif sort_by == 'price from high to low':
            products = products.order_by('-price')
        elif sort_by == 'by name A-Z':
            products = products.order_by('name')
        elif sort_by == 'by name Z-A':
            products = products.order_by('-name')
    context = {'products': products, 'MEDIA_URL': settings.MEDIA_URL}
    return render(request, 'ecomapp/home.html', context)


def customer_creation(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=form.username)
            customer = Customer.objects.create(user=user)
            return








