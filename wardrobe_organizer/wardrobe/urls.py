from django.urls import path
from . import views

app_name = 'wardrobe'

urlpatterns = [
    path('', views.index, name='index'),
    path('items/<int:item_id>/', views.item_detail, name='item_detail'),
    # path('items/create/', views.item_create, name='item_create'),
    path('items/create/', views.ItemCreate.as_view(), name='item_create'),
    path('items/edit/<int:item_id>/', views.item_edit, name='item_edit'),
    path('items/delete/<int:item_id>/', views.item_delete, name='item_delete'),
    path('items/<int:item_id>/add_laundry/', views.add_laundry,
         name='add_laundry'),
    path('items/<int:item_id>/del_laundry/', views.del_laundry,
         name='del_laundry'),
    path('outfits/create/', views.OutfitCreate.as_view(),
         name='outfit_create'),
    path('outfits/<int:outfit_id>/', views.outfit_detail,
         name='outfit_detail'),
    path('outfits/', views.outfit_list, name='outfit_list'),
    path('outfits/edit/<int:outfit_id>/', views.outfit_edit,
         name='outfit_edit'),
    path('outfits/delete/<int:outfit_id>/', views.outfit_delete,
         name='outfit_delete'),
]
