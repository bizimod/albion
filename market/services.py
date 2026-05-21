import requests
from django.utils.dateparse import parse_datetime

from market.models import MarketPrice
from resources.models import Resource


class AlbionMarketService:
    BASE_URL = 'https://europe.albion-online-data.com/api/v2/stats/prices'

    @classmethod
    def fetch_prices(cls, item_ids):
        item_ids_str = ','.join(item_ids)

        url = f'{cls.BASE_URL}/{item_ids_str}.json?qualities=1'

        response = requests.get(url)
        response.raise_for_status()

        return response.json()

    @classmethod
    def update_resource_prices(cls):
        resources = Resource.objects.exclude(item_id__isnull=True)
        item_ids = list(resources.values_list('item_id', flat=True))
        api_data = cls.fetch_prices(item_ids)

        for item_data in api_data:
            item_id = item_data['item_id']
            try:
                resource = Resource.objects.get(item_id=item_id)
            except Resource.DoesNotExist:
                continue
            MarketPrice.objects.update_or_create(
                resource=resource,
                city=item_data['city'],
                defaults={
                    'sell_price_min': item_data['sell_price_min'],
                    'buy_price_max': item_data['buy_price_max'],
                    'updated_at': parse_datetime(
                        item_data['sell_price_min_date']
                    )
                }
            )
