from django.shortcuts import render
from decimal import Decimal
from .forms import RefiningCalculatorForm
from .models import RefiningRecipe
from .services import RefiningCalculator


def refining_calculation(request):
    result = None
    error = None

    if request.method == 'POST':
        form = RefiningCalculatorForm(request.POST)

        try:
            if form.is_valid():
                output_resource = form.cleaned_data['output_resource']
                amount = form.cleaned_data['amount']
                return_rate = form.cleaned_data['return_rate']
                calculation_type = form.cleaned_data['calculation_type']
                buy_city = form.cleaned_data['buy_city']
                sell_city = form.cleaned_data['sell_city']

                recipe = RefiningRecipe.objects.get(output_resource=output_resource)

                if calculation_type == 'full_cycle':
                    ingredients_list = RefiningCalculator.calculate_to_raw(
                        recipe=recipe,
                        desired_amount=amount,
                        return_rate=return_rate
                    )
                    ingredients_for_price = ingredients_list
                else:
                    ingredients_list = RefiningCalculator.calculate_from_output(
                        recipe=recipe,
                        desired_amount=amount,
                        return_rate=return_rate
                    )

                    ingredients_for_price = ingredients_list

                price_result = RefiningCalculator.add_prices_to_result(ingredients=ingredients_for_price, city=buy_city, )
                output_price = RefiningCalculator.get_resource_price(resource=output_resource, city=sell_city)
                output_total = Decimal(amount) * output_price
                profit = output_total - price_result['total_cost']

                result = {
                    'output_resource': output_resource,
                    'desired_amount': amount,
                    'return_rate_percent': return_rate,
                    'calculation_type': calculation_type,
                    'buy_city': buy_city,
                    'sell_city': sell_city,
                    'ingredients': price_result['ingredients'],
                    'total_cost': price_result['total_cost'],
                    'output_price': output_price,
                    'output_total': output_total,
                    'profit': profit,
                }

        except RefiningRecipe.DoesNotExist:
            error = "Recipe for this resource was not found / Рецепт для этого ресурса не найден."
        except ValueError as e:
            error = str(e)
    else:
        form = RefiningCalculatorForm()

    return render(request, 'refining/calculation.html', {'form': form, 'result': result, 'error': error})
