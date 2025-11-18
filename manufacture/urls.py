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
]