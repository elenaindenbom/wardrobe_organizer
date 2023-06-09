from http.client import HTTPResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from .models import Outfit, Item, Laundry, Use
from .forms import ItemForm, OutfitForm
from django.shortcuts import redirect
from django.conf import settings
from datetime import datetime
from .filters import ItemFilter, OutfitFilter, LaundryFilter

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView


CACHE_UPDATE_FREQUENCY = 20


def paginator(items, request):
    """Формирует страницу"""
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
        filter = ItemFilter(request.GET, queryset=user.items.all())
        page_obj = paginator(filter.qs, request)
        context = {
            'title': title,
            'page_obj': page_obj,
            'filter': filter,
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
    laundry = False
    if Laundry.objects.filter(user=request.user).filter(item=item_id):
        laundry = True
    context = {
        'item': item,
        'laundry': laundry,
        # 'form': form,
        # 'comments': comments,
    }
    return render(request, 'wardrobe/item_detail.html', context)


@login_required
def outfit_detail(request, outfit_id):
    """Страница комплекта"""
    outfit = get_object_or_404(Outfit, id=outfit_id)
    items_list = outfit.items.all()
    use_date = Use.objects.filter(outfit=outfit).first()
    already_used = False
    if use_date and datetime.now().date() == use_date.date:
        already_used = True
    page_obj = paginator(items_list, request)
    if outfit.user != request.user:
        return redirect('wardrobe:index')
    context = {
        'outfit': outfit,
        'page_obj': page_obj,
        'use_date': use_date,
        'already_used': already_used,
    }
    return render(request, 'wardrobe/outfit_detail.html', context)


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


# class OutfitCreate(CreateView):
#     """Добавление нового комплекта"""
#     form_class = OutfitForm
#     success_url = reverse_lazy('wardrobe:outfit_list')
#     template_name = 'wardrobe/create_object.html'

#     def form_valid(self, form):
#         new_item = form.save(commit=False)
#         new_item.user = self.request.user
#         new_item.save()
#         return super().form_valid(form)


@login_required
def outfit_create(request):
    """Создание нового комплекта"""
    if request.method == 'POST':
        form = OutfitForm(
            request.POST or None,
            files=request.FILES or None,
        )
        if form.is_valid():
            new_outfit = form.save(commit=False)
            new_outfit.user = request.user
            new_outfit.save()
            return redirect('wardrobe:outfit_list')
        form.fields['items'].queryset = Item.objects.filter(
                                        user=request.user.id)
        return render(request, 'wardrobe/create_object.html', {'form': form})
    form = OutfitForm()
    form.fields['items'].queryset = Item.objects.filter(user=request.user.id)
    return render(request, 'wardrobe/create_object.html', {'form': form})


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
def outfit_edit(request, outfit_id):
    """Редактирование комплекта"""
    outfit = get_object_or_404(Outfit, pk=outfit_id)
    if outfit.user != request.user:
        return redirect('wardrobe:index')

    form = OutfitForm(
        request.POST or None,
        files=request.FILES or None,
        instance=outfit
    )
    form.fields['items'].queryset = Item.objects.filter(user=request.user.id)
    if form.is_valid():
        form.save()
        return redirect('wardrobe:outfit_detail', outfit_id=outfit_id)
    context = {
        'outfit_id': outfit_id,
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


@login_required
def outfit_list(request):
    """Список комплектов"""
    title = 'Коплекты'
    template = 'wardrobe/outfit_list.html'
    user = request.user
    filter = OutfitFilter(request.GET, queryset=user.outfits.all())
    page_obj = paginator(filter.qs, request)
    context = {
        'title': title,
        'page_obj': page_obj,
        'filter': filter,
    }
    return render(request, template, context)


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


@login_required
def outfit_delete(request, outfit_id):
    """Удаление комплекта"""
    outfit = get_object_or_404(Outfit, pk=outfit_id)
    if outfit.user != request.user:
        return redirect('wardrobe:index')
    outfit.delete()
    return redirect('wardrobe:outfit_list')


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
    # extra_context = {
    #     'title': 'Список вещей в стирке',
    #     }

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


@login_required
def outfit_use(request, outfit_id):
    """Добавление информации об использовании комплекта"""
    outfit = get_object_or_404(Outfit, pk=outfit_id)
    Use.objects.create(outfit=outfit)
    outfit.number_of_uses += 1
    outfit.save()
    uses = Use.objects.filter(outfit=outfit)
    if uses.count() > 10:
        uses.earliest().delete()
    return redirect('wardrobe:outfit_detail', outfit_id=outfit_id)


@login_required
def cancel_outfit_use(request, outfit_id):
    """Отмена использования комплекта в текущий день"""
    outfit = get_object_or_404(Outfit, pk=outfit_id)
    use = Use.objects.filter(outfit=outfit).first()
    if use and datetime.now().date() == use.date:
        outfit.number_of_uses -= 1
        outfit.save()
        use.delete()
    return redirect('wardrobe:outfit_detail', outfit_id=outfit_id)


def some_view(request):
    return HTTPResponse('Здесь будет контент')
