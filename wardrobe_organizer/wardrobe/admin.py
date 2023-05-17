from django.contrib import admin

from .models import Item, Care, Type, Usage

admin.site.register(Item)
admin.site.register(Care)
admin.site.register(Type)
admin.site.register(Usage)
