from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, default='Basic User')
    last_name = models.CharField(max_length=100, default='Surname')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Seller(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
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
    image = models.ImageField(upload_to='product_images/')
    description = models.TextField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='product')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='product')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    # products = models.ManyToManyField(Product, related_name='carts')

    def __str__(self):
        return self.owner.username


class Customer(User):
    payment_method = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='customer')

    def __str__(self):
        return self.user



class Review(models.Model):
    text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text












