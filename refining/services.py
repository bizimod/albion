from decimal import Decimal, ROUND_CEILING

from refining.models import RefiningRecipe
from resources.models import ResourceType


class RefiningCalculator:

    @staticmethod
    def _to_decimal(value):
        return Decimal(str(value))

    @staticmethod
    def _round_up(value):
        value = RefiningCalculator._to_decimal(value)
        return value.quantize(Decimal('1'), rounding=ROUND_CEILING)

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
            final_amount = RefiningCalculator._to_decimal(amount_with_return)

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
