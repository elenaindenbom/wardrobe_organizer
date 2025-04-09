from django.shortcuts import render
from wardrobe.filters import ItemFilter
from wardrobe.utils import paginator


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
