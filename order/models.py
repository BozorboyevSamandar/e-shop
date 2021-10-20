from django.db import models
from django.forms import ModelForm
from basic.models import Product
from user.models import Profile


class Shopcart(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.product.title

    @property
    def price(self):
        return self.product.price

    @property
    def amount(self):
        return self.quantity * self.product.price


class ShopcartForm(ModelForm):
    class Meta:
        model = Shopcart
        fields = ['quantity']


class Order(models.Model):
    STATUS = [
        ('New', 'Yangi'),
        ('Accepted', 'Qabul qilingan'),
        ('Preparing', 'Tayyorlanish'),
        ('OnShipping', 'Yetkazib berishga'),
        ('Completed', 'Tugallangan'),
        ('Cancelled', 'Bekor qilingan'),
    ]
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=10, editable=False)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    country = models.CharField(blank=True, max_length=20)
    total = models.FloatField()
    status = models.CharField(max_length=15, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=25)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'country']


class OrderProduct(models.Model):
    STATUS = (
        ('New', 'Yangi'),
        ('Accepted', 'Qabul qilingan'),
        ('Cancelled', 'Bekor qilingan'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=15, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.title}       ---------      {self.user.user.username} ------- {self.order.first_name}"
