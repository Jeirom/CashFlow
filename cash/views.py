from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import CashFlowRecord
from .forms import CashFlowRecordForm

class CashFlowRecordListView(ListView):
    model = CashFlowRecord
    template_name = 'cashflow/cashflowrecord_list.html'

class CashFlowRecordDetailView(DetailView):
    model = CashFlowRecord
    template_name = 'cashflow/cashflowrecord_detail.html'

class CashFlowRecordCreateView(CreateView):
    model = CashFlowRecord
    form_class = CashFlowRecordForm
    template_name = 'cashflow/cashflowrecord_form.html'
    success_url = reverse_lazy('cashflow:list')

class CashFlowRecordUpdateView(UpdateView):
    model = CashFlowRecord
    form_class = CashFlowRecordForm
    template_name = 'cashflow/cashflowrecord_form.html'
    success_url = reverse_lazy('cashflow:list')

class CashFlowRecordDeleteView(DeleteView):
    model = CashFlowRecord
    template_name = 'cashflow/cashflowrecord_confirm_delete.html'
    success_url = reverse_lazy('cashflow:list')
