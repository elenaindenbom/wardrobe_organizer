from django.urls import path, include
from .views import index, item, laundry, outfit

app_name = 'wardrobe'

items_urls = [
    path('<int:item_id>/', item.item_detail, name='item_detail'),
    # path('create/', views.item_create, name='item_create'),
    path('create/', item.ItemCreate.as_view(), name='item_create'),
    path('<int:item_id>/edit/', item.item_edit, name='item_edit'),
    path('<int:item_id>/delete/', item.item_delete, name='item_delete'),
    path('<int:item_id>/add_laundry/', laundry.add_laundry, name='add_laundry'),
    path('<int:item_id>/del_laundry/', laundry.del_laundry, name='del_laundry'),
    path('<int:item_id>/outfits/', item.items_outfits, name='items_outfits')
]

outfits_urls = [
    path('create/', outfit.outfit_create, name='outfit_create'),
    path('<int:outfit_id>/', outfit.outfit_detail, name='outfit_detail'),
    path('', outfit.outfit_list, name='outfit_list'),
    path('<int:outfit_id>/edit/', outfit.outfit_edit, name='outfit_edit'),
    path('<int:outfit_id>/delete/', outfit.outfit_delete, name='outfit_delete'),
    path('<int:outfit_id>/use/', outfit.outfit_use, name='outfit_use'),
    path('<int:outfit_id>/use/cancel/', outfit.cancel_outfit_use,
         name='cancel_outfit_use'),
]

urlpatterns = [
    path('', index.index, name='index'),
    path('items/', include(items_urls)),
    path('outfits/', include(outfits_urls)),
    path('laundry/', laundry.LaundryList.as_view(), name='laundry_list')
]
