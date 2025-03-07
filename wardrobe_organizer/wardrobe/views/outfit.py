from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from ..models.item import Item
from wardrobe.models.outfit import Outfit, Use
from ..forms import OutfitForm
from django.shortcuts import redirect
from datetime import datetime
from ..filters import OutfitFilter
from wardrobe.utils import paginator


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
