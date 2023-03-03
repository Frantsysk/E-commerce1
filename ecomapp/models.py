from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models
from django.db.models import Avg


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.first_name


class PaymentMethod(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payment_methods')
    name = models.CharField(max_length=50)
    card_number = models.CharField(max_length=16, unique=True)
    expiry_month = models.CharField(max_length=2)
    expiry_year = models.CharField(max_length=4)
    cvv = models.CharField(max_length=3)
    billing_address = models.TextField()
    billing_city = models.CharField(max_length=50)
    billing_state = models.CharField(max_length=50)
    billing_zip_code = models.CharField(max_length=10)
    billing_country = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller')
    business_name = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.first_name

    def avg_rate(self):
        return self.products.aggregate(Avg('reviews__rating')).get('reviews__rating__avg') or 'no reviews'


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Attachment(models.Model):
    file = models.FileField(upload_to='attachments')


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='media/')
    description = models.TextField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
    quantity = models.PositiveIntegerField()
    video = models.FileField(upload_to='media/', null=True, blank=True)
    more_images = models.ManyToManyField(Attachment, blank=True, related_name='products')

    def __str__(self):
        return f'{self.name} {self.quantity}'

    def avg_rate(self):
        return self.reviews.aggregate(Avg('rating')).get('rating__avg') or 'no reviews'


class Cart(models.Model):
    owner = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='cart')
    products = models.ManyToManyField(Product, through='CartProduct', related_name='carts', default=[])

    def __str__(self):
        return self.owner.user.username


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.quantity} x {self.product.name} in {self.cart.owner.username} cart'


class Order(models.Model):
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('C', 'Confirmed'),
        ('S', 'Shipped'),
        ('D', 'Delivered'),
        ('X', 'Cancelled'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('Credit', 'Credit Card'),
        ('Paypal', 'Paypal Account'),
        ('Apple Pay', 'Apple Pay Account'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', blank=True)
    date_placed = models.DateTimeField(auto_now_add=True, blank=True)
    products = models.ManyToManyField(Product, through='OrderProduct', blank=True, related_name='orders')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P', blank=True)
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES, default='Credit', blank=True)
    shipping_address = models.TextField(blank=True)
    shipping_city = models.TextField(blank=True)
    shipping_state = models.TextField(blank=True, null=True)
    shipping_zip_code = models.PositiveIntegerField(blank=True, null=True)
    shipping_country = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'Order {self.id} by {self.customer}'


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['customer', 'product'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantity} of {self.product.name} in order {self.order.id}'


