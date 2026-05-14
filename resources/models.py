from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.

class ResourceType(models.TextChoices):
    RAW = 'raw', 'Raw'
    REFINED = 'refined', 'Refined'


class Resource(models.Model):
    item_id = models.CharField(max_length=100, verbose_name='Item ID',unique=True)
    display_name = models.CharField(max_length=100, verbose_name='Display Name')
    tier = models.IntegerField(verbose_name='Tier')
    enchantment = models.IntegerField(default=0, verbose_name='Enchantment')
    type = models.CharField(max_length=10, choices=ResourceType.choices, default=ResourceType.RAW, verbose_name='Type')
    res_image = models.ImageField(upload_to='res_image/%Y/%m/%d/', default=None, blank=True, null=True,
                                  verbose_name='Image')

    def clean(self):
        super().clean()

        # словарь чтоб подсветить нужное поле

        if self.tier < 1 or self.tier > 8:
            raise ValidationError({'tier': 'Tier must be between 1 and 8!'})

        if self.tier < 4 and self.enchantment > 0:
            raise ValidationError({'enchantment': 'Enchanting is not possible for resources below tier 4!'})

        if self.enchantment < 0 or self.enchantment > 4:
            raise ValidationError({'enchantment': 'Enchantment must be between 0 and 4!'})

    class Meta:
        verbose_name = 'Resource'
        verbose_name_plural = 'Resources'
        # constraints = [
        #     models.UniqueConstraint(fields=['item_id', 'tier', 'enchantment', 'type',],
        #                             name='unique_resource_by_name_tier_enchantment_type'),
        # ]

    def __str__(self):
        enchantment_part = f'.{self.enchantment}' if self.enchantment else ''
        title = self.display_name or self.item_id
        return f'{title} T{self.tier}{enchantment_part}'
