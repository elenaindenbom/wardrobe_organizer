import django_filters
from .models.item import Item
from .models.outfit import Outfit
from .models.item_actions import Laundry


class ItemFilter(django_filters.FilterSet):

    class Meta:
        model = Item
        fields = ['type__category', 'type', 'season', 'purpose', 'color',
                  'need_to_buy']
        labels = {
            'type__category': 'Категория',
        }


class OutfitFilter(django_filters.FilterSet):

    class Meta:
        model = Outfit
        fields = ['season', 'purpose']


class LaundryFilter(django_filters.FilterSet):

    class Meta:
        model = Laundry
        fields = ['item__care', 'item__color']
