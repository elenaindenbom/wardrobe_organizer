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
