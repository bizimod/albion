from django.shortcuts import render
from decimal import Decimal
from .forms import RefiningCalculatorForm
from .models import RefiningRecipe
from .services import RefiningCalculator
from resources.models import Resource, ResourceType, ResourceCategory
from market.services import AlbionMarketService

def refining_calculation(request):
    result = None
    error = None

    if request.method == 'POST':
        form = RefiningCalculatorForm(request.POST)

        try:
            if form.is_valid():
                resource_category = form.cleaned_data['resource_category']
                tier = form.cleaned_data['tier']
                enchantment = form.cleaned_data['enchantment']
                output_resource = Resource.objects.get(
                    category=resource_category,
                    tier=tier,
                    enchantment=enchantment,
                    type=ResourceType.REFINED,
                )

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

                resources_to_update = [ingredient['resource'] for ingredient in ingredients_for_price]
                resources_to_update.append(output_resource)
                try:
                    AlbionMarketService.update_prices_for_resources(resources_to_update)
                except Exception as e:
                    price_update_error = f"Prices could not be updated / Не удалось обновить цены: {e}"
                else:
                    price_update_error = None

                price_result = RefiningCalculator.add_prices_to_result(ingredients=ingredients_for_price,
                                                                       city=buy_city, )
                buy_method = form.cleaned_data['buy_method']
                sell_method = form.cleaned_data['sell_method']
                has_premium = form.cleaned_data['has_premium']
                base_total_cost = price_result['total_cost']

                total_cost_with_buy_fee = RefiningCalculator.apply_buy_fee(total_cost=base_total_cost,
                                                                           buy_method=buy_method)

                output_price = RefiningCalculator.get_resource_price(resource=output_resource, city=sell_city)

                output_total = RefiningCalculator._round_money(amount * output_price)

                sell_tax_result = RefiningCalculator.apply_sell_taxes(output_total=output_total,
                                                                      sell_method=sell_method, has_premium=has_premium)

                profit = RefiningCalculator._round_money(sell_tax_result['output_after_tax'] - total_cost_with_buy_fee)

                if total_cost_with_buy_fee > 0:
                    profit_percent = (profit / total_cost_with_buy_fee) * Decimal('100')
                else:
                    profit_percent = Decimal('0')
                result = {
                    'buy_method': buy_method,
                    'sell_method': sell_method,
                    'has_premium': has_premium,

                    'output_resource': output_resource,
                    'desired_amount': amount,
                    'return_rate_percent': return_rate,
                    'calculation_type': calculation_type,

                    'buy_city': buy_city,
                    'sell_city': sell_city,

                    'ingredients': price_result['ingredients'],
                    'base_total_cost': base_total_cost,
                    'total_cost': total_cost_with_buy_fee,
                    'price_update_error': price_update_error,

                    'output_price': output_price,
                    'output_total': output_total,

                    'sell_tax_rate': sell_tax_result['tax_rate'],
                    'sell_tax_amount': sell_tax_result['tax_amount'],
                    'output_after_tax': sell_tax_result['output_after_tax'],

                    'profit': profit,
                    'profit_percent': profit_percent,
                }

        except RefiningRecipe.DoesNotExist:
            error = "Recipe for this resource was not found / Рецепт для этого ресурса не найден."
        except Resource.DoesNotExist:
            error = "Resource with selected parameters was not found / Ресурс с выбранными параметрами не найден."
        except ValueError as e:
            error = str(e)
    else:
        form = RefiningCalculatorForm()

    return render(request, 'refining/calculation.html', {'form': form, 'result': result, 'error': error})
