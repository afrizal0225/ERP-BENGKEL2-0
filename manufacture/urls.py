from django.urls import path
from . import views

urlpatterns = [
    path('stasiunkerja/', views.stasiunkerja_list, name='stasiunkerja_list'),
    path('stasiunkerja/create/', views.stasiunkerja_create, name='stasiunkerja_create'),
    path('stasiunkerja/<int:pk>/update/', views.stasiunkerja_update, name='stasiunkerja_update'),
    path('stasiunkerja/<int:pk>/delete/', views.stasiunkerja_delete, name='stasiunkerja_delete'),
    path('stasiunkerja/bulk/', views.stasiunkerja_bulk_create, name='stasiunkerja_bulk_create'),
    path('stasiunkerja/template/', views.download_stasiunkerja_template, name='download_stasiunkerja_template'),

    path('bom/', views.bom_list, name='bom_list'),
    path('bom/create/', views.bom_create, name='bom_create'),
    path('bom/<str:pk>/update/', views.bom_update, name='bom_update'),
    path('bom/<str:pk>/delete/', views.bom_delete, name='bom_delete'),
    path('bom/<str:pk>/detail/', views.bom_detail, name='bom_detail'),
    path('bomdetail/<int:pk>/update/', views.bomdetail_update, name='bomdetail_update'),
    path('bomdetail/<int:pk>/delete/', views.bomdetail_delete, name='bomdetail_delete'),
    path('bom/bulk/', views.bom_bulk_create, name='bom_bulk_create'),
    path('bom/template/', views.download_bom_template, name='download_bom_template'),

    path('productionorder/', views.productionorder_list, name='productionorder_list'),
    path('productionorder/<str:pk>/update/', views.productionorder_update, name='productionorder_update'),
    path('productionorder/<str:pk>/delete/', views.productionorder_delete, name='productionorder_delete'),
    path('productionorder/<str:pk>/detail/', views.productionorder_detail, name='productionorder_detail'),
    path('productionorder/<str:po_pk>/detail/create/', views.productionorderdetail_create, name='productionorderdetail_create'),
    path('productionorderdetail/<int:pk>/update/', views.productionorderdetail_update, name='productionorderdetail_update'),
    path('productionorderdetail/<int:pk>/delete/', views.productionorderdetail_delete, name='productionorderdetail_delete'),
    path('productionorder/bulk/', views.productionorder_bulk_create, name='productionorder_bulk_create'),
    path('productionorder/template/', views.download_productionorder_template, name='download_productionorder_template'),

    path('spk/', views.spk_list, name='spk_list'),
    path('spk/create/', views.spk_create, name='spk_create'),
    path('spk/<str:pk>/detail/', views.spk_detail, name='spk_detail'),
    path('spk/<str:pk>/approve/', views.spk_approve, name='spk_approve'),
    path('spk/<str:pk>/download/', views.download_spk, name='download_spk'),
    path('spk/<str:pk>/delete/', views.spk_delete, name='spk_delete'),

    path('dashboard/', views.manufacture_dashboard, name='manufacture_dashboard'),
    path('productionprogress/', views.productionprogress_list, name='productionprogress_list'),
    path('productionprogress/create/', views.productionprogress_create, name='productionprogress_create'),
    path('productionprogress/<int:pk>/update/', views.productionprogress_update, name='productionprogress_update'),
    path('productionprogress/<int:pk>/delete/', views.productionprogress_delete, name='productionprogress_delete'),
    path('api/get-products-for-spk/', views.get_products_for_spk, name='get_products_for_spk'),
]