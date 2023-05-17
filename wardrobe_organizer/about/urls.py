from django.urls import path
from . import views


app_name = 'about'

urlpatterns = [
    path('about/', views.AboutAuthorView.as_view(), name='about'),
]
