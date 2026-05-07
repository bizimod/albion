from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Resource


# Register your models here.

@admin.register(Resource)
class ResourcesAdmin(admin.ModelAdmin):
    fields = ['name', 'tier', 'enchantment', 'type', 'res_image']
    # readonly_fields = ['show_image']
    list_display = ['name', 'tier', 'enchantment', 'type', 'show_image']
    search_fields = ['name', 'tier', 'enchantment', 'type']
    list_display_links = ['name']
    list_per_page = 10

    @admin.display(description='Image')
    def show_image(self, obj):
        if obj.res_image:
            return mark_safe(f'<img src="{obj.res_image.url}" width=50')
        return 'No image'
