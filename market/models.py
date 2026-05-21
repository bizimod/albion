from django.db import models
from resources.models import Resource


class MarketPrice(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='market_price')
    city = models.CharField(max_length=50)
    sell_price_min = models.PositiveIntegerField(default=0)
    buy_price_max = models.PositiveIntegerField(default=0)

    updated_at = models.DateTimeField()

    class Meta:
        unique_together = ('resource', 'city')

    def __str__(self):
        return f'{self.resource} - {self.city}: sell {self.sell_price_min}, buy {self.buy_price_max}'
