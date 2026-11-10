from django.db import models
from django.core.exceptions import ValidationError
from resources.models import Resource, ResourceType


class ItemCategory(models.TextChoices):
    BOW = 'bow', 'Bow'
    CROSSBOW = 'crossbow', 'Crossbow'
    SWORD = 'sword', 'Sword'
    AXE = 'axe', 'Axe'
    DAGGER = 'dagger', 'Dagger'
    SPEAR = 'spear', 'Spear'
    STAFF = 'staff', 'Staff'

    CLOTH_ARMOR = 'cloth_armor', 'Cloth Armor'
    LEATHER_ARMOR = 'leather_armor', 'Leather Armor'
    PLATE_ARMOR = 'plate_armor', 'Plate Armor'

    BAG = 'bag', 'Bag'
    CAPE = 'cape', 'Cape'
    TOOL = 'tool', 'Tool'


# Create your models here.
class Artifact(models.Model):
    item_id = models.CharField(max_length=100, verbose_name='Item ID', unique=True)
    display_name = models.CharField(max_length=100, verbose_name='Display Name')
    tier = models.IntegerField(verbose_name='Tier')
    image = models.ImageField(upload_to='artifacts/%Y/%m/%d/', default=None, blank=True, null=True,
                              verbose_name='Image')

    def __str__(self):
        return f'{self.display_name} T{self.tier}'

    class Meta:
        verbose_name = 'Artifact'
        verbose_name_plural = 'Artifacts'


class Item(models.Model):
    item_id = models.CharField(max_length=100, verbose_name='Item ID', unique=True)
    display_name = models.CharField(max_length=100, verbose_name='Display Name')
    tier = models.IntegerField(verbose_name='Tier')
    enchantment = models.IntegerField(default=0, verbose_name='Enchantment')
    category = models.CharField(max_length=30, choices=ItemCategory.choices, verbose_name='Category', )

    image = models.ImageField(upload_to='items/%Y/%m/%d/', default=None, blank=True, null=True,
                              verbose_name='Image')

    def clean(self):
        super().clean()

        if self.tier < 1 or self.tier > 8:
            raise ValidationError({'tier': 'Tier must be between 1 and 8!'})

        if self.tier < 4 and self.enchantment > 0:
            raise ValidationError({'enchantment': 'Enchanting is not possible for items below tier 4!'})

        if self.enchantment < 0 or self.enchantment > 4:
            raise ValidationError({'enchantment': 'Enchantment must be between 0 and 4!'})

    def __str__(self):
        enchantment_part = f'.{self.enchantment}' if self.enchantment else ''
        return f'{self.display_name} T{self.tier}{enchantment_part}'

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'


class CraftingRecipe(models.Model):
    output_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='crafting_recipes',
                                    verbose_name='Output Item')
    output_amount = models.PositiveIntegerField(default=1, verbose_name='Output Amount')

    def __str__(self):
        return f'{self.output_item} - {self.output_amount}'

    class Meta:
        verbose_name = 'Crafting Recipe'
        verbose_name_plural = 'Crafting Recipes'

        constraints = [models.UniqueConstraint(fields=['output_item'], name='unique_crafting_recipe_output_item')]


class CraftingIngredient(models.Model):
    recipe = models.ForeignKey(CraftingRecipe, on_delete=models.CASCADE, related_name='ingredients', )
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, blank=True, null=True,
                                 limit_choices_to={'type': ResourceType.REFINED}, )
    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.PositiveIntegerField(default=1, verbose_name='Amount')

    def clean(self):
        super().clean()

        if self.resource and self.artifact:
            raise ValidationError('Choose either resource or artifact')
        if not self.resource and not self.artifact:
            raise ValidationError('You must choose resource or artifact')

    def __str__(self):
        ingredient = self.resource or self.artifact
        return f'{ingredient} - {self.amount}'
