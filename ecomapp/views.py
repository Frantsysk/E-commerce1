from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Seller, User, Cart, Review, OrderProduct, \
                    Order, CartProduct, Customer, PaymentMethod, Brand, Category, Attachment, Message, Chat
from django.conf import settings
from django.http import Http404, HttpResponseBadRequest, HttpResponseForbidden
from django.db import IntegrityError, transaction
from django.db.models import F, Sum, Case, When, Subquery, Q, OuterRef
from django.urls import reverse
from django.core.paginator import Paginator
from .forms import ReviewForm, PaymentMethodForm, ProductForm
from datetime import datetime
from django.core.mail import send_mail


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if hasattr(user, 'seller'):
                # Redirect to seller account page
                return redirect('seller_account')
            elif hasattr(user, 'customer'):
                # Redirect to customer account page
                return redirect('home')
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

            authenticated_user = authenticate(username=username, password=password)
            login(request, authenticated_user)
            return redirect('seller_account')

        except IntegrityError:

            error_message = "Email already exists. Please use a different email address."
    return render(request, 'ecomapp/seller_register.html')


def seller_account(request):
    try:
        seller = request.user.seller
        products = Product.objects.filter(seller=seller)
    except Seller.DoesNotExist:
        raise Http404("Seller matching query does not exist.")
    context = {'seller': seller, 'products': products}
    return render(request, 'ecomapp/seller_account.html', context)


def seller_details(request, seller_id):
    seller = get_object_or_404(Seller, id=seller_id)
    reviews = Review.objects.filter(product__seller=seller)
    context = {'seller': seller, 'reviews': reviews}
    return render(request, 'ecomapp/seller_detail.html', context)


def edit_seller_account(request):
    seller = request.user.seller
    if request.method == 'POST':
        seller.business_name = request.POST.get('business_name')
        seller.phone = request.POST.get('phone')
        seller.address = request.POST.get('address')
        seller.city = request.POST.get('city')
        seller.state = request.POST.get('state')
        seller.zip_code = request.POST.get('zip_code')
        seller.country = request.POST.get('country')
        seller.save()
        return redirect('seller_account')
    context = {'seller': seller}
    return render(request, 'ecomapp/edit_seller_account.html', context)



@login_required
def add_product(request):
    seller = request.user.seller
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = seller
            product.save()

            for each in form.cleaned_data['attachments']:
                product.more_images.add(Attachment.objects.create(file=each))

            return redirect('seller_account')
    else:
        form = ProductForm()
    context = {'form': form}
    return render(request, 'ecomapp/add_product.html', context)


@login_required
def edit_product(request, product_id):
    seller = request.user.seller
    product = get_object_or_404(Product, id=product_id, seller=seller)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = seller
            product.save()
            for each in form.cleaned_data['attachments']:
                product.more_images.add(Attachment.objects.create(file=each))
            return redirect('edit_product', product_id=product_id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'ecomapp/edit_product.html', {'form': form, 'product': product})


def delete_product(request, pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    return redirect('seller_account')


def home_view(request):
    products = Product.objects.annotate\
        (order_field=Case(When(quantity=0, then=None), default=F('id'))).order_by(F('order_field').desc(nulls_last=True))
    rating = request.GET.get('rating')
    sort_by = request.GET.get('sort_by')
    query = request.GET.get('query')

    if query:
        products = products.filter(name__icontains=query)

    if rating:
        products = products.filter(reviews__rating=rating)

    if sort_by:
        products = products.order_by(sort_by)

    # Set the number of products per page
    per_page = 6

    # Create a Paginator object with the products and number of products per page
    paginator = Paginator(products, per_page)

    # Get the current page number from the request
    page_number = request.GET.get('page', 1)

    # Get the Page object for the current page
    page_obj = paginator.get_page(page_number)

    # Construct the URL for the sort and search form
    url = reverse('home')
    if sort_by:
        url += f'?sort_by={sort_by}'
    if query:
        url += f'{"&" if "?" in url else "?"}query={query}'

    cart_products_count = 0
    if request.user.is_authenticated:
        cart = request.user.customer.cart
        cart_products_count = cart.products.count()

    context = {
        'products': page_obj,
        'MEDIA_URL': settings.MEDIA_URL,
        'sort_by': sort_by,
        'rating': rating,
        'query': query,
        'form_url': url,
        'cart_products_count': cart_products_count
    }

    return render(request, 'ecomapp/home.html', context)


@login_required
def customer_account(request):
    customer = Customer.objects.get(id=request.user.customer.id)
    payment_methods = request.user.customer.payment_methods.all()
    context = {'customer': customer, 'payment_methods': payment_methods}
    return render(request, 'ecomapp/customer_account.html', context)


@login_required
def update_account(request):
    customer = request.user.customer
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
    orders = Order.objects.filter(status='C', customer=request.user.customer)
    is_ordered = orders.filter(products__id=pk).exists()
    reviews = product.reviews.exclude(customer=request.user.customer)
    my_review = product.reviews.filter(customer=request.user.customer).first()
    context = {'product': product, 'MEDIA_URL': settings.MEDIA_URL, 'reviews': reviews, 'my_review': my_review, 'is_ordered': is_ordered}
    return render(request, 'ecomapp/product_detail.html', context)


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
    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)
    if created:
        cart_product.quantity = 1
    else:
        cart_product.quantity += 1
    cart_product.save()
    return redirect('home')


def remove_from_cart(request, pk):
    product = Product.objects.get(id=pk)
    cart = Cart.objects.get(id=request.user.customer.cart.id)
    cart_product = CartProduct.objects.get(cart=cart, product=product)
    cart_product.delete()
    return redirect('cart', cart.id)


def clear_cart(request, card_id):
    cart = Cart.objects.get(id=card_id)
    cart.products.clear()
    return redirect('cart', cart.id)


def buy_product(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(id=request.user.customer.cart.id)
    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)
    if created:
        cart_product.quantity = 1
    else:
        cart_product.quantity += 1
    cart_product.save()
    return redirect('cart', cart.id)


def order_check(request):
    if request.method == 'POST':
        cart = Cart.objects.get(owner=request.user.customer)

        order = Order.objects.create(
            customer=request.user.customer,
            payment_method=request.user.customer.payment_methods,
            status="P",
        )

        for product in cart.products.all():
            quantity = cart.cartproduct_set.get(product=product).quantity
            OrderProduct.objects.create(
                order=order,
                product=product,
                quantity=quantity,
            )

        if 'customer_info' in request.POST:
            info = Customer.objects.get(id=request.POST.get('customer_info'))
            order.shipping_address = info.address
            order.shipping_city = info.city
            order.shipping_state = info.state
            order.shipping_zip_code = info.zip_code
            order.shipping_country = info.country
            order.phone = info.phone
        else:
            order.shipping_address = request.POST.get('address')
            order.shipping_city = request.POST.get('city')
            order.shipping_state = request.POST.get('state')
            order.shipping_zip_code = request.POST.get('zip_code')
            order.shipping_country = request.POST.get('country')
            order.phone = request.POST.get('phone')

        order.save()

        return redirect('checkout', order_id=order.id)

    else:
        cart = Cart.objects.get(owner=request.user.customer)
        products = cart.products.all()
        total_price = sum([product.price for product in products])
        return render(request, 'ecomapp/order_check.html',
                      {'cart': cart, 'products': products, 'total_price': total_price})


def checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    payment_methods = PaymentMethod.objects.filter(owner=request.user.customer)
    form = PaymentMethodForm(request.POST or None)
    if request.method == 'POST':
        if 'payment_method_id' in request.POST:
            payment_method_id = request.POST.get('payment_method_id')
            payment_method = get_object_or_404(PaymentMethod, id=payment_method_id)
            order.payment_type = payment_method
            cart = Cart.objects.get(owner=request.user.customer)
            cart.products.clear()
            return redirect('order_detail', order_id=order.id)
        else:
            if form.is_valid():
                if request.POST.get('consent') == 'no':
                    order.save()
                    cart = Cart.objects.get(owner=request.user.customer)
                    cart.products.clear()
                    return redirect('order_detail', order_id=order.id)
                if request.POST.get('consent') == 'yes':
                    payment_method = form.save(commit=False)
                    payment_method.owner = request.user.customer
                    payment_method.save()
                    order.payment_type = payment_method
                    order.save()
                    cart = Cart.objects.get(owner=request.user.customer)
                    cart.products.clear()
                return redirect('order_detail', order_id=order.id)
    context = {
        'order': order,
        'payment_methods': payment_methods,
        'form': form,
    }
    return render(request, 'ecomapp/checkout.html', context)





# def checkout(request, order_id):
#     form = PaymentMethodForm(request.POST or None)
#     payment_methods = request.user.customer.payment_methods.all()
#     consent = request.POST.get('consent')
#     if request.method == 'POST':
#         if form.is_valid() and consent == 'yes':
#             payment_method = form.save(commit=False)
#             payment_method.owner = request.user.customer
#             payment_method.save()
#         order = Order.objects.get(id=order_id)
#         order.payment_method = 'Credit'
#         order.status = 'C'
#         order.save()
#         cart = Cart.objects.get(owner=request.user.customer)
#         cart.products.clear()
#         return redirect('order_detail', order_id=order.id)
#     else:
#         context = {'form': form, 'payment_methods': payment_methods}
#         return render(request, 'ecomapp/checkout.html', context)


def order_confirmation(request):
    pass


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    total_price = OrderProduct.objects.filter(order=order).aggregate(total=Sum(F('quantity')*F('product__price')))['total']
    context = {'order': order, 'total_price': total_price}
    return render(request, 'ecomapp/order_detail.html', context)


@login_required
def order_history(request):
    customer = request.user.customer
    search_query = request.GET.get('search')

    if search_query:
        orders = Order.objects.filter(customer=customer, products__name__icontains=search_query).annotate(
            total_price=Sum('products__price')).exclude(status='P')
    else:
        orders = Order.objects.filter(customer=customer).annotate(total_price=Sum('products__price')).exclude(
            status='P')

    context = {'orders': orders, 'search_query': search_query}
    return render(request, 'ecomapp/order_history.html', context)


@login_required
def write_review(request, product_id):
    product = Product.objects.filter(orders__products__id=product_id).first()
    if not product:
        raise Http404
    review = product.reviews.filter(customer=request.user.customer).first()
    form = ReviewForm(request.POST or None, instance=review)
    if request.method == "POST":
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.customer = request.user.customer
            review.save()
            return redirect('product_detail', pk=product_id)
    context = {'form': form, 'product': product}
    return render(request, 'ecomapp/write_review.html', context)


@login_required
def add_payment_method(request):
    payment_methods = request.user.customer.payment_methods.all()
    form = PaymentMethodForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            payment_method = form.save(commit=False)
            payment_method.owner = request.user.customer
            payment_method.save()
            return redirect('add_payment_method')
    context = {'form': form, 'payment_methods': payment_methods}
    return render(request, 'ecomapp/add_payment_method.html', context)


@login_required
def remove_image(request, product_id, image_id):
    seller = request.user.seller
    product = get_object_or_404(Product, id=product_id, seller=seller)
    attachment = get_object_or_404(Attachment, id=image_id)
    # product.more_images.remove(attachment)
    attachment.delete()
    return redirect('edit_product', product_id=product_id)


@login_required
def total_sales(request):
    # Get all products for the current seller
    seller_products = Product.objects.filter(seller=request.user.seller)

    # Get all orders for the current seller that have been completed and annotate
    # each order with the total price of all its products
    seller_orders = Order.objects.filter(products__in=seller_products, status='C').annotate(
        total_price=Sum('products__price'))

    # Get filtering parameters from the query string
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    product_name = request.GET.get('product_name')
    customer_name = request.GET.get('customer_name')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    order_by = request.GET.get('order_by', '-date_placed')

    # Apply filters to the orders queryset based on the filtering parameters
    if start_date and end_date:
        # start_date = datetime.strptime(start_date, '%B. %d, %Y').date()  # Change the format here
        # end_date = datetime.strptime(end_date, '%B %d, %Y').date()  # Change the format here
        seller_orders = seller_orders.filter(date_placed__range=[start_date, end_date])

    # if start_date and end_date:
    #     start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    #     end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    #     seller_orders = seller_orders.filter(date_placed__range=[start_date, end_date])

    if product_name:
        seller_orders = seller_orders.filter(products__name__icontains=product_name)

    if customer_name:
        seller_orders = seller_orders.filter(customer__user__username__icontains=customer_name)

    if min_price:
        seller_orders = seller_orders.filter(total_price__gte=int(min_price))

    if max_price:
        seller_orders = seller_orders.filter(total_price__lte=int(max_price))

    # Apply sorting to the orders queryset based on the "order_by" parameter
    seller_orders = seller_orders.order_by(order_by)

    # Create a list of dictionaries containing the sales data to be displayed in the table
    sales_data = []
    for order in seller_orders:
        total_price = order.total_price
        products_list = ', '.join([product.name for product in order.products.all()])
        sales_data.append({
            'id': order.id,
            'customer': order.customer.user.username,
            'date_placed': order.date_placed,
            'order_status': order.status,
            'products': products_list,
            'total_price': total_price,
        })

    # Calculate the total amount earned by the seller from the filtered orders
    total_earned = seller_orders.aggregate(q=Sum('total_price'))['q']

    # Create a dictionary containing all the data needed to render the template
    context = {
        'sales_data': sales_data,
        'total_earned': total_earned,
        'min_price': min_price,
        'max_price': max_price,
        'start_date': start_date,
        'end_date': end_date,
        'product_name': product_name,
        'customer_name': customer_name,
        'order_by': order_by,
    }

    # Render the template with the context data
    return render(request, 'ecomapp/total_sales.html', context)


@login_required
def messages(request):
    if hasattr(request.user, 'seller'):
        my_chats = Chat.objects.filter(seller=request.user.seller)
    elif hasattr(request.user, 'customer'):
        my_chats = Chat.objects.filter(customer=request.user.customer)

    last_messages = Message.objects.filter(chat=OuterRef('pk')).order_by('-timestamp')
    my_chats = my_chats.annotate(
        last_message_text=Subquery(last_messages.values('message')[:1]),
        last_message_timestamp=Subquery(last_messages.values('timestamp')[:1])
    )
    context = {'my_chats': my_chats}
    return render(request, 'ecomapp/messages.html', context)


@login_required
def chat(request, chat_id):
    try:
        if hasattr(request.user, 'seller'):
            chat = Chat.objects.get(pk=chat_id, seller=request.user.seller)
        elif hasattr(request.user, 'customer'):
            chat = Chat.objects.get(pk=chat_id, customer=request.user.customer)
    except Chat.DoesNotExist:
        raise Http404("Chat does not exist")

    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        if message:
            new_message = Message.objects.create(chat=chat, sender=request.user, message=message)
            new_message.save()

    messages = Message.objects.filter(chat=chat).order_by('timestamp')
    context = {'chat': chat, 'messages': messages}
    return render(request, 'ecomapp/chat.html', context)


@login_required
def start_chat(request, seller_id):
    seller = get_object_or_404(Seller, pk=seller_id)
    customer = request.user.customer

    # Check if a chat already exists between the seller and customer
    chat = Chat.objects.filter(seller=seller, customer=customer).first()
    if chat:
        return redirect('chat', chat_id=chat.id)

    # Create a new chat
    chat = Chat.objects.create(seller=seller, customer=customer)

    return redirect('chat', chat_id=chat.id)


def contact_us(request):
    if request.method == 'POST':
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        email_from = request.POST.get('email', '')

        # if subject and message and email_from:
        #     message = f"From: {email_from}\n\n{message}"
        #     send_mail(
        #         subject,
        #         message,
        #         email_from,
        #         [settings.DEFAULT_FROM_EMAIL],
        #         fail_silently=False,
        #     )

        return render(request, 'ecomapp/contact_us_success.html')

    return render(request, 'ecomapp/contact_us.html')


def contact_us_success(request):
    return render(request, 'ecomapp/contact_us_success.html')























