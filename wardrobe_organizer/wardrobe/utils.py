from django.core.paginator import Paginator
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from functools import wraps
...


def paginator(items, request):
    """Формирует страницу"""
    paginator = Paginator(items, settings.ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def owner_only(model, owner_attr='user', redirect_url='wardrobe:index'):
    """Декоратор предоставляет доступ к объекту только владельцу"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            try:
                obj_id = tuple(kwargs.values())[0]
            except IndexError:
                print('Этод декоратор не работае для этой функкции')
                return view_func(request, *args, **kwargs)
            else:
                obj = get_object_or_404(model, id=obj_id)
                if request.user != getattr(obj, owner_attr):
                    messages.error(request, "Доступ запрещен")
                    return redirect(redirect_url)
                return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
