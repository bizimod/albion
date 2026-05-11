from django.core.exceptions import ValidationError
from django.db import models
from resources.models import Resource, ResourceType


class RefiningRecipe(models.Model):
    output_resource = models.ForeignKey(Resource, on_delete=models.CASCADE,
                                        limit_choices_to={'type': ResourceType.REFINED},
                                        related_name='refining_output_resources',
                                        verbose_name='Output resource'
                                        )

    output_amount = models.PositiveIntegerField(default=1, verbose_name='Output amount')

    def clean(self):
        super().clean()

        if self.output_resource and self.output_resource.type != ResourceType.REFINED:
            raise ValidationError({'output_resource': 'The output resource must be refined'})

    def __str__(self):
        return f'{self.output_resource.item_id} : {self.output_resource.display_name} : {self.output_amount}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['output_resource'], name='unique_refining_recipe_output_resource')]


class RefiningIngredient(models.Model):
    recipe = models.ForeignKey(RefiningRecipe, on_delete=models.CASCADE, related_name='ingredients',
                               verbose_name='Recipe')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='refining_ingredients',
                                 verbose_name='Resource')
    amount = models.PositiveIntegerField(default=1, verbose_name='Amount')

    def __str__(self):
        return f'{self.amount} {self.resource} for {self.recipe}'
