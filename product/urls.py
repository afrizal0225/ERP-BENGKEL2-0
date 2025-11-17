from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.items_list, name='items_list'),
    path('products/', views.product_list, name='product_list'),
    path('create/', views.product_create, name='product_create'),
    path('<str:pk>/update/', views.product_update, name='product_update'),
    path('<str:pk>/delete/', views.product_delete, name='product_delete'),
    path('bulk/', views.product_bulk_create, name='product_bulk_create'),
    path('rawmaterials/', views.rawmaterial_list, name='rawmaterial_list'),
    path('rawmaterials/create/', views.rawmaterial_create, name='rawmaterial_create'),
    path('rawmaterials/<str:pk>/update/', views.rawmaterial_update, name='rawmaterial_update'),
    path('rawmaterials/<str:pk>/delete/', views.rawmaterial_delete, name='rawmaterial_delete'),
    path('rawmaterials/bulk/', views.rawmaterial_bulk_create, name='rawmaterial_bulk_create'),
    path('download/product-template/', views.download_product_template, name='download_product_template'),
    path('download/rawmaterial-template/', views.download_rawmaterial_template, name='download_rawmaterial_template'),
]