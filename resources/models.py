from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.

class ResourceType(models.TextChoices):
    RAW = 'raw', 'Raw'
    REFINED = 'refined', 'Refined'


class Resources(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Title')
    tier = models.IntegerField(verbose_name='Tier')
    enchantment = models.IntegerField(default=0, verbose_name='Enchantment')
    type = models.CharField(max_length=10, choices=ResourceType.choices, default=ResourceType.RAW, verbose_name='Type')
    res_image = models.ImageField(upload_to='res_image/%Y/%m/%d/', default=None, blank=True, null=True,
                                  verbose_name='Image')

    def clean(self):
        super().clean()
        if self.tier < 4 and self.enchantment > 0:
            raise ValidationError({
                'enchantment': 'Enchanting is not possible for resources below tier 4!'})
            # словарь чтоб подсветить именно поле Зачарование

    def __str__(self):
        return f"{self.name} Tier: {self.tier} Enchantment: {self.enchantment} Type: {self.type}"
