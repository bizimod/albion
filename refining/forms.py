from django import forms
from resources.models import Resource, ResourceType,ResourceCategory

CITY_CHOICES = [
    ('Bridgewatch', 'Bridgewatch'),
    ('Fort Sterling', 'Fort Sterling'),
    ('Lymhurst', 'Lymhurst'),
    ('Martlock', 'Martlock'),
    ('Thetford', 'Thetford'),
    ('Caerleon', 'Caerleon'),
    ('Brecilien', 'Brecilien'),
]

CALCULATION_CHOICES = [
    ('full_cycle', 'Full craft cycle / Полный цикл (с нуля)'),
    ('last_step', 'Last step only / Только последний шаг'),
]

BUY_METHOD_CHOICES = [
    ('buy_direct', 'Buy directly / Купить напрямую'),
    ('buy_order', 'Buy order / Покупка через ордер'),
]

SELL_METHOD_CHOICES = [
    ('sell_direct', 'Sell directly / Продажа напрямую'),
    ('sell_order', 'Sell order / Продажа через ордер'),
]


class RefiningCalculatorForm(forms.Form):
    resource_category = forms.ChoiceField(choices=ResourceCategory.choices, label='Resource type / Тип ресурса' )
    tier = forms.ChoiceField( choices=[(tier, f'T{tier}') for tier in range(2, 9)], label='Tier / Тир' )
    enchantment = forms.ChoiceField( choices=[ (0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), ], initial=0, label='Enchantment / Зачарование' )

    amount = forms.DecimalField(min_value=1, initial=1, label='Amount / Количество')

    return_rate = forms.DecimalField(min_value=0, max_value=100, decimal_places=2, initial=15.25,
                                     label='Return rate / Возврат ресурсов (%)')

    calculation_type = forms.ChoiceField(choices=CALCULATION_CHOICES, initial='full_cycle',
                                         label='Calculation mode / Режим расчета')

    buy_city = forms.ChoiceField(choices=CITY_CHOICES, label='Buy city / Город покупки')

    sell_city = forms.ChoiceField(choices=CITY_CHOICES, label='Sell city / Город продажи')

    buy_method = forms.ChoiceField(choices=BUY_METHOD_CHOICES, label='Buy method / Способ покупки')

    sell_method = forms.ChoiceField(choices=SELL_METHOD_CHOICES, label='Sell method / Способ продажи')

    has_premium = forms.BooleanField(required=False, initial=True, label='Premium / Премиум')
