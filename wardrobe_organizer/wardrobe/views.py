from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from .models import Outfit, Item
# from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.conf import settings

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
        items_list = Item.objects.filter(user=request.user)
        page_obj = paginator(items_list, request)
        context = {
            'title': title,
            'page_obj': page_obj,
        }
        return render(request, template, context)
    template = 'about/about.html'
    return render(request, template)
