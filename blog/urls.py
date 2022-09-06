from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('posts/<slug:slug>/', views.post_detail, name = 'detail'),
    path('cat/<slug:category_slug>', views.category_show, name= 'category_show' ),
]