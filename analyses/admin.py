from django.contrib import admin
from .models import Analysis, AnalysisType

admin.site.register(Analysis)
admin.site.register(AnalysisType)