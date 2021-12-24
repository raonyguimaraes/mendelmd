from enum import Enum
from django.db import models
from django.contrib.auth.models import User


class OrderType(Enum):
    SUBSCRIPTION = 'Subscription'
    PRODUCT = 'Product'

    def __str__(self):
        return str(self.value)

    @classmethod
    def choices(cls):
        return [(x.value, x.name) for x in cls]


class PaymentStatus(Enum):
    PROCESSING = 'Processing'
    PAID = 'Paid'
    REFUSED = 'Refused'
    CANCELED = 'Canceled'

    def __str__(self):
        return str(self.value)

    @classmethod
    def choices(cls):
        return [(x.value, x.name) for x in cls]


class Product(models.Model):
    name = models.CharField(max_length=191)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to='products_images/', blank=True)
    is_subscription = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    cart_id = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    def __str__(self):
        return "{}:{}".format(self.product.name, self.id)

    def update_quantity(self, quantity):
        self.quantity = self.quantity + quantity
        self.save()

    def total_cost(self):
        return self.quantity * self.price


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=20,
                                      choices=PaymentStatus.choices(),
                                      default=PaymentStatus.PROCESSING.__str__())
    order_type = models.CharField(max_length=20,
                                  choices=OrderType.choices(),
                                  default=OrderType.SUBSCRIPTION.__str__())

    def __str__(self):
        return "{}:{}:{}".format(self.id, self.order_type, self.user.email)

    def total_cost(self):
        return sum([li.cost() for li in self.lineitem_set.all()])


class LineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}:{}".format(self.product.name, self.id)

    def cost(self):
        return self.price * self.quantity
