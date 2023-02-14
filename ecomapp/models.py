from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller')
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='media/')
    description = models.TextField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products_brand')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products_category')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products_seller')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    products = models.ManyToManyField(Product, through='CartProduct', related_name='carts', default=[])

    def __str__(self):
        return self.owner.username


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantity} x {self.product.name} in {self.cart.owner.username} cart'


# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
#     payment_method = models.CharField(max_length=100)
#     address = models.TextField()
#     phone = models.CharField(max_length=20, blank=True)
#     cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='customer_cart')
#
#     def __str__(self):
#         return self.username


class Review(models.Model):
    text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    date_placed = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through='OrderProduct')
    payment_method = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'Order {self.id} by {self.customer.username}'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantity} of {self.product.name} in order {self.order.id}'



