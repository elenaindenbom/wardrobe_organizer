from django.urls import path
from . import views

app_name = 'wardrobe'

urlpatterns = [
    path('', views.index, name='index'),
    path('items/<int:item_id>/', views.item_detail, name='item_detail'),
    # path('items/create/', views.item_create, name='item_create'),
    path('items/create/', views.ItemCreate.as_view(), name='item_create'),
    path('outfits/create/', views.OutfitCreate.as_view(),
         name='outfit_create'),
    path('items/edit/<int:item_id>/', views.item_edit, name='item_edit'),
    path('items/delete/<int:item_id>/', views.item_delete, name='item_delete'),
]
