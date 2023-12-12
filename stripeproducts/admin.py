from django.contrib import admin
from .models import MyStripeModel, Plan

admin.site.register(MyStripeModel)
admin.site.register(Plan)
