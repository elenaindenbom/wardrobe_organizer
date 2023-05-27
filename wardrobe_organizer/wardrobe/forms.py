from django import forms
from .models import Item, Outfit


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('image', 'name', 'need_to_buy', 'care', 'price', 'season',
                  'type', 'purpose', 'color', 'storage_place', 'note')
        help_texts = {
            'storage_place': ('Укажите место хранения вещи,'
                              'чтобы ничего не терялось.'),
            'need_to_buy': ('Вы можете добавлять в гардероб вещи, '
                            'которых у вас пока нет, '
                            'но они нужны для завершения образа. '
                            'Присвойте им отметку "Нужно докупить" '
                            'со значением "Да". Иначе оставте "Нет".'),
            'care': 'Зажмите ctrl чтобы выбрать несколько вариантов.'
        }


class OutfitForm(forms.ModelForm):
    class Meta:
        model = Outfit
        fields = ('image', 'name', 'items', 'season',
                  'purpose', 'min_temperature', 'max_temperature', 'note')
        help_texts = {
            'items': 'Зажмите ctrl чтобы выбрать несколько вариантов.'
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     user = kwargs.get('user')
    #     item_qs = Item.objects.filter(user=user.id)
    #     self.fields['items'].queryset = item_qs
