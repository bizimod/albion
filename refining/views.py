from django.shortcuts import render
from .forms import RefiningCalculatorForm
from .models import RefiningRecipe
from .services import RefiningCalculator


def refining_calculation(request):
    result = None
    error = None

    if request.method == 'POST':
        try:
            form = RefiningCalculatorForm(request.POST)

            if form.is_valid():
                output_resource = form.cleaned_data['output_resource']
                amount = form.cleaned_data['amount']
                return_rate = form.cleaned_data['return_rate']

                recipe = RefiningRecipe.objects.get(output_resource=output_resource)

                raw_result = RefiningCalculator.calculate_to_raw(
                    recipe=recipe,
                    desired_amount=amount,
                    return_rate=return_rate
                )

                result = {
                    'output_resource': output_resource,
                    'desired_amount': amount,
                    'return_rate_percent': return_rate,
                    'raw_ingredients': raw_result.values(),
                }

        except RefiningRecipe.DoesNotExist:
            error = "Recipe for this resource was not found / Рецепт для этого ресурса не найден."
        except ValueError as e:
            error = str(e)

    return render(request, 'refining/calculation.html', {'form': form, 'result': result, 'error': error})
