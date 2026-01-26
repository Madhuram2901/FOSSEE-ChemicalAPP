from django.contrib import admin
from .models import UploadedDataset


@admin.register(UploadedDataset)
class UploadedDatasetAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded_at')
    readonly_fields = ('summary',)
