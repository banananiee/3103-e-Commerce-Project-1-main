from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from datetime import datetime
from MorphoCraft.bcryptpasswordhasher import BCryptPasswordHasher
import os
import string
import secrets


class User(AbstractUser):
    class Meta:
        db_table = "user"

    email = models.EmailField(unique=True)
    salt = models.CharField(max_length=63, blank=True, null=True)
    account_creation_date = models.DateTimeField(default=datetime.now)
    verified = models.BooleanField(default=False)
    verification_url = models.CharField(max_length=63, blank=True, null=True)

    ROLE_CHOICES = (
        ("user", "User"),
        ("owner", "Owner"),
        ("admin", "Admin"),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")

    # Specify custom related names for groups and user_permissions
    groups = models.ManyToManyField(Group, blank=True, related_name="custom_user_set")
    user_permissions = models.ManyToManyField(
        Permission, blank=True, related_name="custom_user_permissions_set"
    )

    def set_password(self, raw_password):
        length = 63
        pepper = os.getenv("SECRET_PEPPER")
        hasher = BCryptPasswordHasher()
        new_salt = "".join(
            secrets.choice(string.ascii_letters + string.digits) for _ in range(length)
        )

        new_salted_password = pepper + raw_password + new_salt
        hashed_password = hasher.encode(new_salted_password, hasher.salt())

        self.salt = new_salt
        self.password = hashed_password


class Log(models.Model):
    class Meta:
        db_table = "log"

    log_id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User, db_column="user_id", on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=15)
    login_time = models.DateTimeField(default=datetime.now)
    login_success = models.BooleanField()
    details = models.TextField(max_length=2047, blank=True, null=True)


class Product(models.Model):
    class Meta:
        db_table = "product"

    name = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    type = models.CharField(max_length=63, null=True)
    image = models.ImageField(null=True)
    top_color = models.CharField(max_length=63)
    bottom_color = models.CharField(max_length=63)
    length = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


class Order(models.Model):
    class Meta:
        db_table = "order"

    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    class Meta:
        db_table = "order_item"

    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    class Meta:
        db_table = "shipping_address"

    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=255, null=False)
    unit_number = models.CharField(max_length=63, null=False)
    zipcode = models.CharField(max_length=63, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class Review(models.Model):
    class Meta:
        db_table = "reviews"

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"
