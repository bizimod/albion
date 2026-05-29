from decimal import Decimal, ROUND_CEILING, ROUND_HALF_UP

from refining.models import RefiningRecipe
from resources.models import ResourceType
from market.models import MarketPrice


class RefiningCalculator:

    @staticmethod
    def _to_decimal(value):
        return Decimal(str(value))

    @staticmethod
    def _round_up(value):
        value = RefiningCalculator._to_decimal(value)
        return value.quantize(Decimal('1'), rounding=ROUND_CEILING)

    @staticmethod
    def _round_money(value):
        value = RefiningCalculator._to_decimal(value)
        return value.quantize(Decimal('1'), rounding=ROUND_HALF_UP)

    @staticmethod
    def _get_return_rate_decimal(return_rate):
        return RefiningCalculator._to_decimal(return_rate) / Decimal('100')

    @staticmethod
    def _get_crafts_count(recipe, desired_amount):
        desired_amount = RefiningCalculator._to_decimal(desired_amount)
        return desired_amount / Decimal(recipe.output_amount)

    @staticmethod
    def _apply_return_rate(amount, return_rate):
        base_amount = RefiningCalculator._to_decimal(amount)
        return_rate_decimal = RefiningCalculator._get_return_rate_decimal(return_rate)
        return base_amount * (Decimal('1') - return_rate_decimal)

    @staticmethod
    def get_market_tax_rate(has_premium):
        if has_premium:
            return Decimal('0.04')
        return Decimal('0.08')

    @staticmethod
    def get_order_fee_rate():
        return Decimal('0.025')

    @staticmethod
    def apply_buy_fee(total_cost, buy_method):
        total_cost = RefiningCalculator._to_decimal(total_cost)
        if buy_method == 'buy_order':
            return total_cost * (Decimal('1') + RefiningCalculator.get_order_fee_rate())
        return RefiningCalculator._round_money(total_cost)

    @staticmethod
    def apply_sell_taxes(output_total, sell_method, has_premium):
        output_total = RefiningCalculator._to_decimal(output_total)
        market_tax_rate = RefiningCalculator.get_market_tax_rate(has_premium)
        total_tax_rate = market_tax_rate

        if sell_method == 'sell_order':
            total_tax_rate += RefiningCalculator.get_order_fee_rate()

        tax_amount = output_total * total_tax_rate
        output_after_tax = output_total - tax_amount

        return {
            'tax_rate': total_tax_rate * Decimal('100'),
            'tax_amount': RefiningCalculator._round_money(tax_amount),
            'output_after_tax': RefiningCalculator._round_money(output_after_tax),
        }

    @staticmethod
    def calculate_from_output(recipe, desired_amount, return_rate):
        """
        Считает, сколько ингредиентов нужно,
        чтобы получить desired_amount готового ресурса.
        """
        desired_amount = RefiningCalculator._to_decimal(desired_amount)
        craft_count = RefiningCalculator._get_crafts_count(recipe=recipe, desired_amount=desired_amount)

        result = []

        for ingredient in recipe.ingredients.all():
            base_amount = Decimal(ingredient.amount) * craft_count
            amount_with_return = RefiningCalculator._apply_return_rate(amount=base_amount, return_rate=return_rate)
            final_amount = RefiningCalculator._round_up(amount_with_return)

            result.append({
                'resource': ingredient.resource,
                'amount': final_amount,
            })
        return result

    @staticmethod
    def calculate_to_raw(recipe, desired_amount, return_rate, visited=None):
        """
        Рекурсивно раскладывает готовый ресурс до сырых ресурсов.
        Например:
        T3_PLANKS -> T2_PLANKS + T3_WOOD
        T2_PLANKS -> T2_WOOD

        Итог:
        T2_WOOD
        T3_WOOD
        """
        if visited is None:
            visited = set()
        if recipe.id in visited:
            raise ValueError(f'Cycle detected in recipe: {recipe}')

        visited.add(recipe.id)

        craft_count = RefiningCalculator._get_crafts_count(recipe=recipe, desired_amount=desired_amount)
        result = {}

        for ingredient in recipe.ingredients.all():
            base_amount = Decimal(ingredient.amount) * craft_count
            amount_with_return = RefiningCalculator._apply_return_rate(amount=base_amount, return_rate=return_rate)

            resource = ingredient.resource

            if resource.type == ResourceType.RAW:
                if resource.id not in result:
                    result[resource.id] = {'resource': resource, 'amount': Decimal('0')}

                result[resource.id]['amount'] += amount_with_return

            elif resource.type == ResourceType.REFINED:
                try:
                    sub_recipe = RefiningRecipe.objects.get(output_resource=resource)
                except RefiningRecipe.DoesNotExist:
                    raise ValueError(f'No refining recipe found for refined resource: {resource}')

                sub_result = RefiningCalculator.calculate_to_raw(recipe=sub_recipe,
                                                                 desired_amount=amount_with_return,
                                                                 return_rate=return_rate,
                                                                 visited=visited.copy())

                for data in sub_result:
                    resource_id = data['resource'].id
                    if resource_id not in result:
                        result[resource_id] = {'resource': data['resource'], 'amount': Decimal('0')}
                    result[resource_id]['amount'] += data['amount']

        for resource_data in result.values():
            resource_data['amount'] = RefiningCalculator._round_up(resource_data['amount'])

        sorted_result = sorted(result.values(), key=lambda item: item['resource'].tier)

        return sorted_result

    @staticmethod
    def add_prices_to_result(ingredients, city):
        total_cost = Decimal('0')

        priced_ingredients = []
        for ingredient in ingredients:
            resource = ingredient['resource']
            amount = ingredient['amount']

            try:
                market_price = MarketPrice.objects.get(city=city, resource=resource)
                price = Decimal(market_price.sell_price_min or 0)
                updated_at = market_price.updated_at

            except MarketPrice.DoesNotExist:
                price = Decimal('0')
                updated_at = None

            total = RefiningCalculator._round_money(amount * price)

            priced_ingredients.append({
                'resource': resource,
                'amount': amount,
                'price': price,
                'total': total,
                'updated_at': updated_at,
            })
            total_cost += total
        return {
            'ingredients': priced_ingredients,
            'total_cost': RefiningCalculator._round_money(total_cost),
        }

    @staticmethod
    def get_resource_price(resource, city):
        try:
            market_price = MarketPrice.objects.get(
                resource=resource,
                city=city
            )
            return Decimal(market_price.sell_price_min or 0)

        except MarketPrice.DoesNotExist:
            return Decimal('0')
