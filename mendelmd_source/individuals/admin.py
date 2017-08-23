from django.contrib import admin
from individuals.models import ControlGroup, UserGroup, Individual
# Register your models here.
admin.site.register(ControlGroup)
admin.site.register(UserGroup)

admin.site.register(Individual)
