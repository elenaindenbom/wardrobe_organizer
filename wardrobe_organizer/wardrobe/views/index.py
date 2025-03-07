from django.core.paginator import Paginator
from django.shortcuts import render
from django.conf import settings
from wardrobe.filters import ItemFilter


def paginator(items, request):
    """Формирует страницу"""
    paginator = Paginator(items, settings.ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


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
