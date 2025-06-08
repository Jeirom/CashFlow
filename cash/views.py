import json

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import CashFlow, Category, Type, Status, Subcategory
from .forms import CashFlowForm
from django.contrib import messages
from django.utils import timezone


class CashFlowListView(ListView):
    model = CashFlow
    template_name = 'cashflow/cashflow_list.html'
    context_object_name = 'cashflows'
    paginate_by = 20  # добавляем пагинацию
    ordering = ['-date_created']

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user).select_related(
            'status', 'type', 'category', 'subcategory'
        )

        # Фильтр по дате
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        if date_from:
            qs = qs.filter(date_created__gte=date_from)
        if date_to:
            qs = qs.filter(date_created__lte=date_to)

        # Фильтр по статусу
        status_id = self.request.GET.get('status')
        if status_id:
            qs = qs.filter(status_id=status_id)

        # Фильтр по типу
        type_id = self.request.GET.get('type')
        if type_id:
            qs = qs.filter(type_id=type_id)

        # Фильтр по категории
        category_id = self.request.GET.get('category')
        if category_id:
            qs = qs.filter(category_id=category_id)

        # Фильтр по подкатегории
        subcategory_id = self.request.GET.get('subcategory')
        if subcategory_id:
            qs = qs.filter(subcategory_id=subcategory_id)

        # Фильтр по сумме
        amount_min = self.request.GET.get('amount_min')
        amount_max = self.request.GET.get('amount_max')
        if amount_min:
            qs = qs.filter(amount__gte=amount_min)
        if amount_max:
            qs = qs.filter(amount__lte=amount_max)

        # Возможность сортировки
        ordering = self.request.GET.get('ordering', '-date_created')
        qs = qs.order_by(ordering)

        return qs


class CashFlowCreateView(CreateView):
    """Представление для создания новой записи о движении денежных средств"""
    model = CashFlow
    form_class = CashFlowForm
    template_name = 'cashflow/cashflow_form.html'
    success_url = reverse_lazy('home')

    def get_initial(self):
        initial = super().get_initial()
        initial['date_created'] = timezone.now().date()
        return initial

    def form_valid(self, form):
        messages.success(self.request, 'Запись успешно создана')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subcategories = list(Subcategory.objects.values('id', 'name', 'category_id'))
        context['subcategories_json'] = json.dumps(subcategories)
        context['today'] = timezone.now().date()
        return context


class CashFlowUpdateView(UpdateView):
    """Представление для редактирования записи о движении денежных средств"""
    model = CashFlow
    form_class = CashFlowForm
    template_name = 'cashflow/cashflow_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, 'Запись успешно обновлена')
        return super().form_valid(form)


class CashFlowDeleteView(DeleteView):
    """Представление для удаления записи о движении денежных средств"""
    model = CashFlow
    template_name = 'cashflow/cashflow_confirm_delete.html'
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Запись успешно удалена')
        return super().delete(request, *args, **kwargs)


class CashFlowDetailView(DetailView):
    """Представление для удаления записи о движении денежных средств"""
    model = CashFlow
    template_name = 'cashflow/cashflow_detail.html'
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Запись успешно удалена')
        return super().delete(request, *args, **kwargs)


########################################################################################################################
#                                                Status View's                                                         #
########################################################################################################################


class StatusListView(ListView):
    model = Status
    template_name = 'status_list.html'
    context_object_name = 'statuses'


class StatusDetailView(DetailView):
    model = Status
    template_name = 'status_detail.html'
    context_object_name = 'status'


class StatusCreateView(CreateView):
    model = Status
    fields = ['name']
    template_name = 'status_form.html'
    success_url = reverse_lazy('status_list')


class StatusUpdateView(UpdateView):
    model = Status
    fields = ['name']
    template_name = 'status_form.html'
    success_url = reverse_lazy('status_list')


class StatusDeleteView(DeleteView):
    model = Status
    template_name = 'status_confirm_delete.html'
    success_url = reverse_lazy('status_list')


########################################################################################################################
#                                                Type View's                                                           #
########################################################################################################################


class TypeListView(ListView):
    model = Type
    template_name = 'type_list.html'
    context_object_name = 'types'

class TypeDetailView(DetailView):
    model = Type
    template_name = 'type_detail.html'
    context_object_name = 'type'

class TypeCreateView(CreateView):
    model = Type
    fields = ['name']
    template_name = 'type_form.html'
    success_url = reverse_lazy('type_list')

class TypeUpdateView(UpdateView):
    model = Type
    fields = ['name']
    template_name = 'type_form.html'
    success_url = reverse_lazy('type_list')

class TypeDeleteView(DeleteView):
    model = Type
    template_name = 'type_confirm_delete.html'
    success_url = reverse_lazy('type_list')


########################################################################################################################
#                                                Category View's                                                       #
########################################################################################################################


class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'

class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']
    template_name = 'category_form.html'
    success_url = reverse_lazy('category_list')

class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']
    template_name = 'category_form.html'
    success_url = reverse_lazy('category_list')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('category_list')


########################################################################################################################
#                                                Subcategory View's                                                    #
########################################################################################################################


class SubcategoryListView(ListView):
    model = Subcategory
    template_name = 'subcategory_list.html'
    context_object_name = 'subcategories'

class SubcategoryDetailView(DetailView):
    model = Subcategory
    template_name = 'subcategory_detail.html'
    context_object_name = 'subcategory'

class SubcategoryCreateView(CreateView):
    model = Subcategory
    fields = ['name', 'category']
    template_name = 'subcategory_form.html'
    success_url = reverse_lazy('subcategory_list')

class SubcategoryUpdateView(UpdateView):
    model = Subcategory
    fields = ['name', 'category']
    template_name = 'subcategory_form.html'
    success_url = reverse_lazy('subcategory_list')

class SubcategoryDeleteView(DeleteView):
    model = Subcategory
    template_name = 'subcategory_confirm_delete.html'
    success_url = reverse_lazy('subcategory_list')