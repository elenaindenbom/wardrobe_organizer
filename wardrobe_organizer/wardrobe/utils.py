from django.core.paginator import Paginator
from django.conf import settings
...


def paginator(items, request):
    """Формирует страницу"""
    paginator = Paginator(items, settings.ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


# def owner_only(func, object):
#     def check_user(request, *args, **kwargs):
#         if request.user == object.user:
#             return func(request, *args, **kwargs)
#         return redirect('wardrobe:index')
#     return check_user