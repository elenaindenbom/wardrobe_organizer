from django.contrib import admin

from .models import Item, Care, Type, Purpose

admin.site.register(Care)
admin.site.register(Purpose)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'type', 'purpose', 'user')
    list_filter = ('name', 'color', 'season', 'type', 'purpose', 'user')
    search_fields = ('name',)
    readonly_fields = ('number_of_uses',)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
