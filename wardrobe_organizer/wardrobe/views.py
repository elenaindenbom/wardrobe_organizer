from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from .models import Outfit, Item
from .forms import ItemForm, OutfitForm
from django.shortcuts import redirect
from django.conf import settings

from django.urls import reverse_lazy
from django.views.generic import CreateView


CACHE_UPDATE_FREQUENCY = 20


def paginator(items, request):
    """Формирует страницу с постами"""
    paginator = Paginator(items, settings.ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


@cache_page(CACHE_UPDATE_FREQUENCY, key_prefix='index_page')
def index(request):
    """Главная страница"""
    title = 'Гардероб'
    if request.user.is_authenticated:
        template = 'wardrobe/index.html'
        user = request.user
        items_list = user.items.all()
        page_obj = paginator(items_list, request)
        context = {
            'title': title,
            'page_obj': page_obj,
        }
        return render(request, template, context)
    template = 'about/about.html'
    return render(request, template)


@login_required
def item_detail(request, item_id):
    """Страница предмета"""
    item = get_object_or_404(Item, id=item_id)
    if item.user != request.user:
        return redirect('wardrobe:index')
    # form = CommentForm()
    # comments = item.comments.select_related('author').all()
    context = {
        'item': item,
        # 'form': form,
        # 'comments': comments,
    }
    return render(request, 'wardrobe/item_detail.html', context)


@login_required
def item_create(request):
    """Добавление нового предмета"""
    if request.method == 'POST':
        form = ItemForm(
            request.POST or None,
            files=request.FILES or None,
        )
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            return redirect('wardrobe:item_detail', item_id=new_item.id)
        return render(request, 'wardrobe/create_item.html', {'form': form})
    form = ItemForm()
    return render(request, 'wardrobe/create_item.html', {'form': form})


class ItemCreate(CreateView):
    form_class = ItemForm
    success_url = reverse_lazy('wardrobe:index')
    template_name = 'wardrobe/create_object.html'

    def form_valid(self, form):
        new_item = form.save(commit=False)
        new_item.user = self.request.user
        new_item.save()
        return super().form_valid(form)


class OutfitCreate(CreateView):
    form_class = OutfitForm
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
    return render(request, 'wardrobe/create_item.html', context)


@login_required
def item_delete(request, item_id):
    """Удаление предмета"""
    item = get_object_or_404(Item, pk=item_id)
    if item.user != request.user:
        return redirect('wardrobe:index')
    item.delete()
    return redirect('wardrobe:index')
