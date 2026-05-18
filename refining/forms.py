from django import forms
from resources.models import Resource, ResourceType


class RefiningCalculatorForm(forms.Form):
    output_resource = forms.ModelChoiceField(queryset=Resource.objects.filter(type=ResourceType.REFINED),
                                             label='Output resource / Что хочешь получить', )

    amount = forms.DecimalField(min_value=1, initial=1, label='Amount / Количество')

    return_rate = forms.DecimalField(min_value=0, max_value=100, decimal_places=2, initial=0,
                                     label='Return rate / Возврат ресурсов (%)')
