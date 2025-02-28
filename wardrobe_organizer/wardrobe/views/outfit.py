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


@login_required
def outfit_delete(request, outfit_id):
    """Удаление комплекта"""
    outfit = get_object_or_404(Outfit, pk=outfit_id)
    if outfit.user != request.user:
        return redirect('wardrobe:index')
    outfit.delete()
    return redirect('wardrobe:outfit_list')
