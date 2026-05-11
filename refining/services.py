from decimal import Decimal

class RefiningCalculation:
    @staticmethod
    def calculate_from_output(recipe,desired_amount,return_rate):
        """
        Считает, сколько ингредиентов нужно,
        чтобы получить desired_amount готового ресурса.
        """
        desired_amount = Decimal(str(desired_amount))

        return_rate_percent = Decimal(str(return_rate))
        return_rate_decimal = Decimal(str(return_rate)) / Decimal('100')

        craft_count = desired_amount / Decimal(recipe.output_amount)

        result = []

        for ingredient in recipe.ingredients.all():
            base_amount = Decimal(ingredient.amount) * craft_count
            amount_with_return = base_amount * (Decimal('1') - return_rate_decimal)

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
