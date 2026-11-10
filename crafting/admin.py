from django.contrib import admin
from django.utils.safestring import mark_safe
from crafting.models import Artifact, Item, CraftingRecipe, CraftingIngredient


class CraftingIngredientInline(admin.TabularInline):
    model = CraftingIngredient
    extra = 1

class ImagePreviewAdminMixin:
    @admin.display(description='Image')
    def show_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width=50>')
        return 'No image'


@admin.register(CraftingRecipe)
class CraftingRecipeAdmin(admin.ModelAdmin):
    inlines = [CraftingIngredientInline]
    list_display = ('output_item', 'output_amount')
    search_fields = ('output_item__item_id', 'output_item__display_name')
    list_filter = ('output_item__tier', 'output_item__enchantment', 'output_item__category')


@admin.register(Artifact)
class ArtifactAdmin(ImagePreviewAdminMixin,admin.ModelAdmin):
    list_display = ('item_id', 'display_name', 'tier','show_image')
    search_fields = ('item_id', 'display_name')
    list_filter = ('tier',)


@admin.register(Item)
class ItemAdmin(ImagePreviewAdminMixin,admin.ModelAdmin):
    list_display = ('item_id', 'display_name', 'tier', 'enchantment', 'category','show_image')
    search_fields = ('item_id', 'display_name', 'category')
    list_filter = ('tier', 'enchantment', 'category',)


@admin.register(CraftingIngredient)
class CraftingIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'resource', 'artifact', 'amount')
    search_fields = ('recipe__output_item__display_name', 'resource__display_name', 'artifact__display_name',)
