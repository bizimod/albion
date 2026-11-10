from django.db import models
from resources.models import Resource
from crafting.models import Artifact,Item

class MarketPrice(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='market_price')
    city = models.CharField(max_length=50)
    sell_price_min = models.PositiveIntegerField(default=0)
    buy_price_max = models.PositiveIntegerField(default=0)

    updated_at = models.DateTimeField()

    class Meta:
        verbose_name = 'Resource Market Price'
        verbose_name_plural = 'Resource Market Prices'

        constraints = [
            models.UniqueConstraint(
                fields=['resource', 'city'],
                name='unique_together_resource_and_city'
            )
        ]

    def __str__(self):
        return f'{self.resource} - {self.city}: sell {self.sell_price_min}, buy {self.buy_price_max}'

class ItemMarketPrice(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='market_prices')
    city = models.CharField(max_length=50)
    sell_price_min = models.PositiveIntegerField(default=0)
    buy_price_max = models.PositiveIntegerField(default=0)

    updated_at = models.DateTimeField()

    class Meta:
        verbose_name = 'Item Market Price'
        verbose_name_plural = 'Item Market Prices'

        constraints = [
            models.UniqueConstraint(
                fields=['item', 'city'],
                name='unique_together_item_and_city'
            )
        ]

    def __str__(self):
        return f'{self.item} - {self.city}: sell {self.sell_price_min}, buy {self.buy_price_max}'

class ArtifactMarketPrice(models.Model):
    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE, related_name='market_prices')
    city = models.CharField(max_length=50)
    sell_price_min = models.PositiveIntegerField(default=0)
    buy_price_max = models.PositiveIntegerField(default=0)

    updated_at = models.DateTimeField()

    class Meta:
        verbose_name = 'Artifact Market Price'
        verbose_name_plural = 'Artifact Market Prices'

        constraints = [
            models.UniqueConstraint(
                fields=['artifact', 'city'],
                name='unique_together_artifact_and_city'
            )
        ]

    def __str__(self):
        return f'{self.artifact} - {self.city}: sell {self.sell_price_min}, buy {self.buy_price_max}'