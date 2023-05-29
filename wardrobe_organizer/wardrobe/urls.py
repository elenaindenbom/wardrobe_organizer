from django.urls import path, include
from . import views

app_name = 'wardrobe'

items_urls = [
    path('<int:item_id>/', views.item_detail, name='item_detail'),
    # path('create/', views.item_create, name='item_create'),
    path('create/', views.ItemCreate.as_view(), name='item_create'),
    path('<int:item_id>/edit/', views.item_edit, name='item_edit'),
    path('<int:item_id>/delete/', views.item_delete, name='item_delete'),
    path('<int:item_id>/add_laundry/', views.add_laundry, name='add_laundry'),
    path('<int:item_id>/del_laundry/', views.del_laundry, name='del_laundry'),
    path('<int:item_id>/outfits/', views.items_outfits, name='items_outfits')
]

outfits_urls = [
    path('create/', views.outfit_create, name='outfit_create'),
    path('<int:outfit_id>/', views.outfit_detail, name='outfit_detail'),
    path('', views.outfit_list, name='outfit_list'),
    path('<int:outfit_id>/edit/', views.outfit_edit, name='outfit_edit'),
    path('<int:outfit_id>/delete/', views.outfit_delete, name='outfit_delete'),
    path('<int:outfit_id>/use/', views.outfit_use, name='outfit_use'),
    path('<int:outfit_id>/use/cancel/', views.cancel_outfit_use,
         name='cancel_outfit_use'),
]

urlpatterns = [
    path('', views.index, name='index'),
    path('items/', include(items_urls)),
    path('outfits/', include(outfits_urls)),
    path('laundry/', views.LaundryList.as_view(), name='laundry_list')
]
