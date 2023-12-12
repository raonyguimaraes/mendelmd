from django.db import models

# Create your models here.
from django.contrib import admin
from .models import MyStripeModel, Plan

admin.site.register(MyStripeModel)

class Plan(models.Model):
    # your existing fields here
    amount = models.IntegerField()  # assuming this is your price in cents

    @property
    def human_readable_price(self):
        return "${:.2f}".format(self.amount / 100)

class Subscription(models.Model):
    # your existing fields here
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

admin.site.register(Plan)
