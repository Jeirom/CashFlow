import os

from django.urls import path
from cash.views import (
    CashFlowListView,
    CashFlowDetailView,
    CashFlowCreateView,
    CashFlowUpdateView,
    CashFlowDeleteView,
    manage_all,
    StatusListView, StatusDetailView, StatusCreateView, StatusUpdateView, StatusDeleteView,
    TypeListView, TypeDetailView, TypeCreateView, TypeUpdateView, TypeDeleteView,
    CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    SubcategoryListView, SubcategoryDetailView, SubcategoryCreateView, SubcategoryUpdateView, SubcategoryDeleteView,
)
from cash.apps import CashConfig
app_name = 'cashflow' if os.getenv("DEBUG") == "True" else CashConfig.name


urlpatterns = [
    path("", CashFlowListView.as_view(), name="list"), # main-страница
    path("<int:pk>/", CashFlowDetailView.as_view(), name="detail"),
    path("add/", CashFlowCreateView.as_view(), name="add"),
    path("<int:pk>/edit/", CashFlowUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", CashFlowDeleteView.as_view(), name="delete"), # до этого момента урлы - CRUD CashFlow
    path("manage/", manage_all, name="manage"), # вьюшка редактирования остальных моделей

    # Status URLs
    path('statuses/', StatusListView.as_view(), name='status_list'),
    path('statuses/<int:pk>/', StatusDetailView.as_view(), name='status_detail'),
    path('statuses/add/', StatusCreateView.as_view(), name='status_create'),
    path('statuses/<int:pk>/edit/', StatusUpdateView.as_view(), name='status_update'),
    path('statuses/<int:pk>/delete/', StatusDeleteView.as_view(), name='status_delete'),

    # Type URLs
    path('types/', TypeListView.as_view(), name='type_list'),
    path('types/<int:pk>/', TypeDetailView.as_view(), name='type_detail'),
    path('types/add/', TypeCreateView.as_view(), name='type_create'),
    path('types/<int:pk>/edit/', TypeUpdateView.as_view(), name='type_update'),
    path('types/<int:pk>/delete/', TypeDeleteView.as_view(), name='type_delete'),

    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('categories/add/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),

    # Subcategory URLs
    path('subcategories/', SubcategoryListView.as_view(), name='subcategory_list'),
    path('subcategories/<int:pk>/', SubcategoryDetailView.as_view(), name='subcategory_detail'),
    path('subcategories/add/', SubcategoryCreateView.as_view(), name='subcategory_create'),
    path('subcategories/<int:pk>/edit/', SubcategoryUpdateView.as_view(), name='subcategory_update'),
    path('subcategories/<int:pk>/delete/', SubcategoryDeleteView.as_view(), name='subcategory_delete'),
]
