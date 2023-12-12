from django.contrib import admin

from .models import SSHKey, CloudKey

admin.site.register(SSHKey)


class CloudKeyAdmin(admin.ModelAdmin):
    list_display = ["name", "cloudprovider"]


admin.site.register(CloudKey, CloudKeyAdmin)
