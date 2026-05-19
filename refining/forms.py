from django import forms
from resources.models import Resource, ResourceType


class RefiningCalculatorForm(forms.Form):
    output_resource = forms.ModelChoiceField(queryset=Resource.objects.filter(type=ResourceType.REFINED),
                                             label='Output resource / Что хочешь получить', )

    amount = forms.DecimalField(min_value=1, initial=1, label='Amount / Количество')

    return_rate = forms.DecimalField(min_value=0, max_value=100, decimal_places=2, initial=15.25,
                                     label='Return rate / Возврат ресурсов (%)')

    CALCULATION_CHOICES = [
        ('full_cycle', 'Full craft cycle / Полный цикл (с нуля)'),
        ('last_step', 'Last step only / Только последний шаг'),
    ]
    calculation_type = forms.ChoiceField(choices=CALCULATION_CHOICES, initial='full_cycle',
                                         label='Calculation mode / Режим расчета')
