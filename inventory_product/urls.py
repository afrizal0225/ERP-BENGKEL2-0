from django.urls import path
from . import views

urlpatterns = [
    # Penerimaan
    path('penerimaan/', views.penerimaan_list, name='penerimaan_list'),
    path('penerimaan/create/', views.penerimaan_create, name='penerimaan_create'),
    path('penerimaan/<str:pk>/update/', views.penerimaan_update, name='penerimaan_update'),
    path('penerimaan/<str:pk>/delete/', views.penerimaan_delete, name='penerimaan_delete'),
    path('penerimaan/bulk/', views.penerimaan_bulk_create, name='penerimaan_bulk_create'),
    path('penerimaan/<str:pk>/details/', views.penerimaan_detail_list, name='penerimaan_detail_list'),
    path('penerimaan/<str:pk>/details/add/', views.penerimaan_detail_create, name='penerimaan_detail_create'),
    path('download/penerimaan-template/', views.download_penerimaan_template, name='download_penerimaan_template'),

    # Keluar
    path('keluar/', views.keluar_list, name='keluar_list'),
    path('keluar/create/', views.keluar_create, name='keluar_create'),
    path('keluar/<str:pk>/update/', views.keluar_update, name='keluar_update'),
    path('keluar/<str:pk>/delete/', views.keluar_delete, name='keluar_delete'),
    path('keluar/bulk/', views.keluar_bulk_create, name='keluar_bulk_create'),
    path('keluar/<str:pk>/details/', views.keluar_detail_list, name='keluar_detail_list'),
    path('keluar/<str:pk>/details/add/', views.keluar_detail_create, name='keluar_detail_create'),
    path('download/keluar-template/', views.download_keluar_template, name='download_keluar_template'),

    # Inventory
    path('inventory/products/', views.inventory_product_list, name='inventory_product_list'),
    path('inventory/rawmaterials/', views.inventory_rawmaterial_list, name='inventory_rawmaterial_list'),

    # Raw Material Penerimaan
    path('penerimaan-rawmaterial/', views.penerimaan_rawmaterial_list, name='penerimaan_rawmaterial_list'),
    path('penerimaan-rawmaterial/create/', views.penerimaan_rawmaterial_create, name='penerimaan_rawmaterial_create'),
    path('penerimaan-rawmaterial/<str:pk>/update/', views.penerimaan_rawmaterial_update, name='penerimaan_rawmaterial_update'),
    path('penerimaan-rawmaterial/<str:pk>/delete/', views.penerimaan_rawmaterial_delete, name='penerimaan_rawmaterial_delete'),
    path('penerimaan-rawmaterial/bulk/', views.penerimaan_rawmaterial_bulk_create, name='penerimaan_rawmaterial_bulk_create'),
    path('penerimaan-rawmaterial/<str:pk>/details/', views.penerimaan_rawmaterial_detail_list, name='penerimaan_rawmaterial_detail_list'),
    path('penerimaan-rawmaterial/<str:pk>/details/add/', views.penerimaan_rawmaterial_detail_create, name='penerimaan_rawmaterial_detail_create'),
    path('download/penerimaan-rawmaterial-template/', views.download_penerimaan_rawmaterial_template, name='download_penerimaan_rawmaterial_template'),

    # Raw Material Keluar
    path('keluar-rawmaterial/', views.keluar_rawmaterial_list, name='keluar_rawmaterial_list'),
    path('keluar-rawmaterial/create/', views.keluar_rawmaterial_create, name='keluar_rawmaterial_create'),
    path('keluar-rawmaterial/<str:pk>/update/', views.keluar_rawmaterial_update, name='keluar_rawmaterial_update'),
    path('keluar-rawmaterial/<str:pk>/delete/', views.keluar_rawmaterial_delete, name='keluar_rawmaterial_delete'),
    path('keluar-rawmaterial/bulk/', views.keluar_rawmaterial_bulk_create, name='keluar_rawmaterial_bulk_create'),
    path('keluar-rawmaterial/<str:pk>/details/', views.keluar_rawmaterial_detail_list, name='keluar_rawmaterial_detail_list'),
    path('keluar-rawmaterial/<str:pk>/details/add/', views.keluar_rawmaterial_detail_create, name='keluar_rawmaterial_detail_create'),
    path('download/keluar-rawmaterial-template/', views.download_keluar_rawmaterial_template, name='download_keluar_rawmaterial_template'),
]