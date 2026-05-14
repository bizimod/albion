from decimal import Decimal


class RefiningCalculation:

    @staticmethod
    def _to_decimal(value):
        return Decimal(str(value))

    @staticmethod
    def _get_return_rate_decimal(return_rate):
        return RefiningCalculation._to_decimal(return_rate) / Decimal('100')

    @staticmethod
    def _get_crafts_count(recipe, desired_amount):
        desired_amount = RefiningCalculation._to_decimal(desired_amount)
        return desired_amount / Decimal(recipe.output_amount)

    @staticmethod
    def _apply_return_rate(amount, return_rate):
        base_amount = RefiningCalculation._to_decimal(amount)
        return_rate_decimal = RefiningCalculation._get_return_rate_decimal(return_rate)
        return base_amount * (Decimal('1') - return_rate_decimal)

    @staticmethod
    def calculate_from_output(recipe, desired_amount, return_rate):
        """
        Считает, сколько ингредиентов нужно,
        чтобы получить desired_amount готового ресурса.
        """
        desired_amount = RefiningCalculation._to_decimal(desired_amount)
        return_rate_percent = RefiningCalculation._to_decimal(return_rate)

        craft_count = RefiningCalculation._get_crafts_count(recipe=recipe, desired_amount=desired_amount)

        result = []

        for ingredient in recipe.ingredients.all():
            base_amount = Decimal(ingredient.amount) * craft_count
            amount_with_return = RefiningCalculation._apply_return_rate(amount=base_amount, return_rate=return_rate)

            result.append({
                'resource': ingredient.resource,
                'amount_without_return': base_amount,
                'amount_with_return': amount_with_return,
            })

        return {
            'output_resource': recipe.output_resource,
            'desired_amount': desired_amount,
            'return_rate_percent': return_rate_percent,
            'ingredients': result,
        }
