import requests
from django.utils.dateparse import parse_datetime

from market.models import MarketPrice, ItemMarketPrice, ArtifactMarketPrice
from resources.models import Resource
from crafting.models import Artifact, Item


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
    def _update_prices_by_item_ids(cls, item_ids, source_model, price_model, fk_field):
        if not item_ids:
            return
        api_data = cls.fetch_prices(item_ids)

        for item_data in api_data:
            item_id = item_data['item_id']
            try:
                obj = source_model.objects.get(item_id=item_id)
            except source_model.DoesNotExist:
                continue

            update_at = (parse_datetime(item_data.get('sell_price_min_date')) or parse_datetime(
                item_data.get('buy_price_max_date')))

            price_model.objects.update_or_create(
                **{
                    fk_field: obj,
                    "city": item_data["city"],
                },
                defaults={
                    "sell_price_min": item_data["sell_price_min"] or 0,
                    "buy_price_max": item_data["buy_price_max"] or 0,
                    "updated_at": update_at,
                },
            )

    @classmethod
    def update_resource_prices(cls):
        # обновляет все ресурсы в базе данных
        resources = Resource.objects.exclude(item_id__isnull=True)
        item_ids = list(resources.values_list('item_id', flat=True))
        cls._update_prices_by_item_ids(
            item_ids=item_ids,
            source_model=Resource,
            price_model=MarketPrice,
            fk_field='resource',
        )

    @classmethod
    def update_item_prices(cls):
        items = Item.objects.exclude(item_id__isnull=True)
        item_ids = list(items.values_list("item_id", flat=True))

        cls._update_prices_by_item_ids(
            item_ids=item_ids,
            source_model=Item,
            price_model=ItemMarketPrice,
            fk_field="item",
        )

    @classmethod
    def update_artifact_prices(cls):
        artifacts = Artifact.objects.exclude(item_id__isnull=True)
        item_ids = list(artifacts.values_list("item_id", flat=True))

        cls._update_prices_by_item_ids(
            item_ids=item_ids,
            source_model=Artifact,
            price_model=ArtifactMarketPrice,
            fk_field="artifact",
        )

    @classmethod
    def update_prices_for_resources(cls, resources):
        # Обновляет цены только для ресурсов, участвующих в переработке
        item_ids = [resource.item_id for resource in resources if resource.item_id]

        cls._update_prices_by_item_ids(
            item_ids=item_ids,
            source_model=Resource,
            price_model=MarketPrice,
            fk_field='resource',
        )