from django.contrib import admin
from .models import S3Credential, Provider

admin.site.register(S3Credential)
admin.site.register(Provider)
