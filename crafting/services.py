from crafting.models import CraftingRecipe, CraftingIngredient
from market.models import MarketPrice, ArtifactMarketPrice, ItemMarketPrice


class CraftingCalculator:

    @staticmethod
    def calculate(item, city='Martlock'):
        recipe = CraftingRecipe.objects.select_related(
            'output_item'
        ).get(output_item=item)

        ingredients = recipe.ingredients.select_related(
            'resource',
            'artifact',
        )

        total_cost = 0
        ingredients_data = []

        for ingredient in ingredients:
            price = 0

            if ingredient.resource:
                price = MarketPrice.objects.get(
                    resource=ingredient.resource,
                    city=city
                ).buy_price_max

            elif ingredient.artifact:
                price = ArtifactMarketPrice.objects.get(
                    artifact=ingredient.artifact,
                    city=city
                ).buy_price_max

            total = price * ingredient.amount
            total_cost += total

            ingredients_data.append({
                "name": str(ingredient.resource or ingredient.artifact),
                "amount": ingredient.amount,
                "price": price,
                "total": total,
            })
        item_price = ItemMarketPrice.objects.get(item=item, city=city).sell_price_min
        profit = total_cost - item_price
        roi = 0

        if total_cost > 0:
            roi = profit / total_cost * 100
        return {
            "ingredients": ingredients_data,
            "total_cost": total_cost,
            "item_price": item_price,
            "profit": profit,
            "roi": roi,
        }
