from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from wardrobe.models import Laundry, Item
from wardrobe.filters import LaundryFilter
from django.views.generic import ListView
from django.shortcuts import redirect


@login_required
def add_laundry(request, item_id):
    """Добавление в список стирки"""
    item = get_object_or_404(Item, pk=item_id)
    Laundry.objects.get_or_create(
        user=request.user,
        item=item
    )
    return redirect('wardrobe:item_detail', item_id=item_id)


@login_required
def del_laundry(request, item_id):
    """Добавление в список стирки"""
    item = get_object_or_404(Item, pk=item_id)
    laundry = get_object_or_404(Laundry, item=item, user=request.user)
    laundry.delete()
    return redirect('wardrobe:item_detail', item_id=item_id)


class LaundryList(ListView):
    model = Laundry
    template_name = 'wardrobe/laundry_list.html'
    extra_context = {
        'title': 'Список вещей в стирке',
        }

    def get_queryset(self):
        return Laundry.objects.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список вещей в стирке'
        context['filter'] = LaundryFilter(
            self.request.GET,
            queryset=Laundry.objects.filter(user=self.request.user)
        )
        return context
