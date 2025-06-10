import os

from django.urls import path
from cash.views import (
    CashFlowListView,
    CashFlowDetailView,
    CashFlowCreateView,
    CashFlowUpdateView,
    CashFlowDeleteView,
    manage_all,
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
]
