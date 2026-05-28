from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Resource


# Register your models here.

@admin.register(Resource)
class ResourcesAdmin(admin.ModelAdmin):
    fields = ['item_id', 'display_name', 'tier', 'enchantment', 'type', 'res_image', 'category']
    # readonly_fields = ['show_image']
    list_display = ['item_id', 'display_name', 'tier', 'enchantment', 'type', 'category', 'show_image']
    list_filter = ['type','category',]
    search_fields = ['item_id', 'display_name', 'tier', 'enchantment', 'type']
    list_display_links = ['item_id']
    list_per_page = 10

    @admin.display(description='Image')
    def show_image(self, obj):
        if obj.res_image:
            return mark_safe(f'<img src="{obj.res_image.url}" width=50')
        return 'No image'
