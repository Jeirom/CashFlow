from django.urls import path
from .views import (
    CashFlowListView,
    CashFlowDetailView,
    CashFlowCreateView,
    CashFlowUpdateView,
    CashFlowDeleteView,
)

app_name = 'cashflow'

urlpatterns = [
    path('', CashFlowListView.as_view(), name='list'),
    path('<int:pk>/', CashFlowDetailView.as_view(), name='detail'),
    path('add/', CashFlowCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', CashFlowUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', CashFlowDeleteView.as_view(), name='delete'),
]
