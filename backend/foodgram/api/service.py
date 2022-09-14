from django.db.models import Sum
from django.http import HttpResponse

from food.models import AmountIngredient
from foodgram.settings import SHOPPING_CART_FILENAME


def shopping_cart(user):
    ingredients = AmountIngredient.objects.filter(
        recipe__shopping_cart__user=user
    ).values(
        'ingredients__name',
        'ingredients__measurement_unit',
    ).annotate(
        value=Sum('amount')
    ).order_by('ingredients__name')
    response = HttpResponse(
        content_type='text/plain',
        charset='utf-8',
    )
    response['Content-Disposition'] = (
        f'attachment; filename={SHOPPING_CART_FILENAME}'
    )
    response.write('Список продуктов к покупке:\n')
    for ingredient in ingredients:
        response.write(
            f'- {ingredient["ingredients__name"]} '
            f'- {ingredient["value"]} '
            f'{ingredient["ingredients__measurement_unit"]}\n'
        )
    return response