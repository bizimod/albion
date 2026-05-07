from django.contrib import admin
from .models import RefiningRecipe, RefiningIngredient


class RefiningIngredientInline(admin.TabularInline):
    model = RefiningIngredient
    extra = 1

#добавление рецепта с несколькими составляющими благодаря inlines
@admin.register(RefiningRecipe)
class RefiningRecipeAdmin(admin.ModelAdmin):
    inlines = [RefiningIngredientInline]
    list_display = ('output_resource', 'output_amount')
    search_fields = ('output_resource__name',)
    list_filter = ('output_resource__tier', 'output_resource__enchantment')

#все ингридиенты рецептов
@admin.register(RefiningIngredient)
class RefiningIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'resource', 'amount')
    search_fields = ('resource__name', 'recipe__output_resource__name')
    list_filter = ('resource__tier', 'resource__enchantment', 'resource__type')
