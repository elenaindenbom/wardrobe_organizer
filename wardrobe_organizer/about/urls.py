from django.urls import path
from . import views


app_name = 'about'

urlpatterns = [
    path('about/', views.AboutProjectView.as_view(), name='about'),
]
