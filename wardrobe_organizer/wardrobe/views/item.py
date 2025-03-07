from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from wardrobe.models import Item, Laundry
from wardrobe.forms import ItemForm
from django.shortcuts import redirect
from wardrobe.filters import OutfitFilter
from wardrobe.utils import paginator

from django.urls import reverse_lazy
from django.views.generic import CreateView


@login_required
def item_detail(request, item_id):
    """Страница предмета"""
    item = get_object_or_404(Item, id=item_id)
    if item.user != request.user:
        return redirect('wardrobe:index')
    laundry = False
    if Laundry.objects.filter(user=request.user).filter(item=item_id):
        laundry = True
    context = {
        'item': item,
        'laundry': laundry,
    }
    return render(request, 'wardrobe/item_detail.html', context)


# @login_required
# def item_create(request):
#     """Добавление нового предмета"""
#     if request.method == 'POST':
#         form = ItemForm(
#             request.POST or None,
#             files=request.FILES or None,
#         )
#         if form.is_valid():
#             new_item = form.save(commit=False)
#             new_item.user = request.user
#             new_item.save()
#             return redirect('wardrobe:item_detail', item_id=new_item.id)
#         return render(request, 'wardrobe/create_item.html', {'form': form})
#     form = ItemForm()
#     return render(request, 'wardrobe/create_item.html', {'form': form})


class ItemCreate(CreateView):
    """Добавление нового предмета"""
    form_class = ItemForm
    success_url = reverse_lazy('wardrobe:index')
    template_name = 'wardrobe/create_object.html'

    def form_valid(self, form):
        new_item = form.save(commit=False)
        new_item.user = self.request.user
        new_item.save()
        return super().form_valid(form)


@login_required
def item_edit(request, item_id):
    """Редактирование предмета"""
    item = get_object_or_404(Item, pk=item_id)
    if item.user != request.user:
        return redirect('wardrobe:index')

    form = ItemForm(
        request.POST or None,
        files=request.FILES or None,
        instance=item
    )
    if form.is_valid():
        form.save()
        return redirect('wardrobe:item_detail', item_id=item_id)
    context = {
        'item_id': item_id,
        'form': form,
        'is_edit': True,
    }
    return render(request, 'wardrobe/create_object.html', context)


@login_required
def item_delete(request, item_id):
    """Удаление предмета"""
    item = get_object_or_404(Item, pk=item_id)
    if item.user != request.user:
        return redirect('wardrobe:index')
    item.delete()
    return redirect('wardrobe:index')


def items_outfits(request, item_id):
    """Вывод комплектов содержащих предмет"""
    template = 'wardrobe/outfit_list.html'
    item = get_object_or_404(Item, pk=item_id)
    outfit_list = item.outfits.filter(user=request.user)
    filter = OutfitFilter(request.GET, queryset=outfit_list)
    page_obj = paginator(filter.qs, request)
    title = f'{item.name}. Все комплекты:'
    context = {
        'title': title,
        'page_obj': page_obj,
        'filter': filter,
    }
    return render(request, template, context)
