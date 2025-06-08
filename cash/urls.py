from django.urls import path
from cash.views import (
    CashFlowRecordListView,
    CashFlowRecordDetailView,
    CashFlowRecordCreateView,
    CashFlowRecordUpdateView,
    CashFlowRecordDeleteView,
)

app_name = 'cashflow'

urlpatterns = [
    path('', CashFlowRecordListView.as_view(), name='list'),
    path('<int:pk>/', CashFlowRecordDetailView.as_view(), name='detail'),
    path('add/', CashFlowRecordCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', CashFlowRecordUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', CashFlowRecordDeleteView.as_view(), name='delete'),
]
