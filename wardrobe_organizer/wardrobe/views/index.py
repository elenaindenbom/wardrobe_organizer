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