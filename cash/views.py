import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from .models import CashFlow, Category, Type, Status, Subcategory
from .forms import CashFlowForm, StatusForm, TypeForm, CategoryForm, SubcategoryForm
from django.contrib import messages
from django.utils import timezone


class CashFlowListView(LoginRequiredMixin, ListView):
    """🌟 CashFlowListView — ваш щит и меч в мире финансов.
    Фильтруйте, сортируйте, управляйте — и делайте деньги своим оружием.
    Погружайтесь в детали, управляйте потоками — и достигайте новых высот!"""

    login_url = 'users:login'  # URL, куда перенаправлять неавторизованных
    redirect_field_name = 'next'  # стандартное имя GET-параметра для возврата
    model = CashFlow
    template_name = "cashflow/cashflow_list.html"
    context_object_name = "cashflows"
    paginate_by = 20  # добавляем пагинацию
    ordering = ["-date_created"] # сортируем пл дате создания записи

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .filter(user=self.request.user) # Выгружаем юзеру только его собственные записи.
            .select_related("status", "type", "category", "subcategory")
        )

        # Фильтр по дате
        date_from = self.request.GET.get("date_from")
        date_to = self.request.GET.get("date_to")
        if date_from:
            qs = qs.filter(date_created__gte=date_from)
        if date_to:
            qs = qs.filter(date_created__lte=date_to)

        # Фильтр по статусу
        status_id = self.request.GET.get("status")
        if status_id:
            qs = qs.filter(status_id=status_id)

        # Фильтр по типу
        type_id = self.request.GET.get("type")
        if type_id:
            qs = qs.filter(type_id=type_id)

        # Фильтр по категории
        category_id = self.request.GET.get("category")
        if category_id:
            qs = qs.filter(category_id=category_id)

        # Фильтр по подкатегории
        subcategory_id = self.request.GET.get("subcategory")
        if subcategory_id:
            qs = qs.filter(subcategory_id=subcategory_id)

        # Фильтр по сумме
        amount_min = self.request.GET.get("amount_min")
        amount_max = self.request.GET.get("amount_max")
        if amount_min:
            qs = qs.filter(amount__gte=amount_min)
        if amount_max:
            qs = qs.filter(amount__lte=amount_max)

        # Возможность сортировки
        ordering = self.request.GET.get("ordering", "-date_created")
        qs = qs.order_by(ordering)

        return qs

    def get_context_data(self, **kwargs):
        """
        Наделяем вьюшку контекстами всех его подопечных.
        """
        context = super().get_context_data(**kwargs)
        context["statuses"] = Status.objects.all()
        context["types"] = Type.objects.all()
        context["categories"] = Category.objects.all()
        context["subcategories"] = Subcategory.objects.all()
        return context


class CashFlowCreateView(CreateView):
    """Представление для создания новой записи о движении денежных средств"""

    model = CashFlow
    form_class = CashFlowForm
    template_name = "cashflow/cashflow_form.html"
    success_url = reverse_lazy("cashflow:list")

    def get_initial(self):
        initial = super().get_initial()
        initial["date_created"] = timezone.now().date()
        return initial

    def form_valid(self, form):
        # Перед сохранением присваиваем текущего пользователя
        cashflow = form.save(commit=False)
        cashflow.user = self.request.user
        cashflow.save()
        messages.success(self.request, "Запись успешно создана")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subcategories = list(Subcategory.objects.values("id", "name", "category_id"))
        context["subcategories_json"] = json.dumps(subcategories)
        context["today"] = timezone.now().date()
        context["statuses"] = Status.objects.all()
        context["types"] = Type.objects.all()
        context["categories"] = Category.objects.all()
        context["subcategories"] = Subcategory.objects.all()
        return context


class CashFlowUpdateView(UpdateView):
    """
    Представление для редактирования существующей записи о движении денежных средств.

    Позволяет пользователю внести изменения в выбранную запись. После успешного
    обновления отображает сообщение и возвращает к списку всех записей.
    """
    model = CashFlow
    form_class = CashFlowForm
    template_name = "cashflow/cashflow_form.html"
    success_url = reverse_lazy("cashflow:list")

    def form_valid(self, form):
        messages.success(self.request, "Запись успешно обновлена")
        return super().form_valid(form)


class CashFlowDeleteView(DeleteView):
    """
    Представление для удаления записи о движении денежных средств.

    Позволяет пользователю подтвердить удаление выбранной записи. После удаления
    отображает сообщение и перенаправляет на список всех записей.
    """
    model = CashFlow
    template_name = "cashflow/cashflow_confirm_delete.html"
    success_url = reverse_lazy("cashflow:list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Запись успешно удалена")
        return super().delete(request, *args, **kwargs)


class CashFlowDetailView(DetailView):
    """
    Представление для просмотра подробной информации о конкретной записи.

    Позволяет пользователю ознакомиться с деталями выбранной операции. Не предназначено
    для редактирования или удаления, только для просмотра.
    """
    model = CashFlow
    template_name = "cashflow/cashflow_detail.html"
    success_url = reverse_lazy("/list/")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Запись успешно удалена")
        return super().delete(request, *args, **kwargs)


########################################################################################################################
#                                                Status View's                                                         #
########################################################################################################################


class StatusListView(ListView):
    model = Status
    template_name = "status_list.html"
    context_object_name = "statuses"


class StatusDetailView(DetailView):
    model = Status
    template_name = "status_detail.html"
    context_object_name = "status"


class StatusCreateView(CreateView):
    model = Status
    fields = ["name"]
    template_name = "status_form.html"
    success_url = reverse_lazy("status_list")


class StatusUpdateView(UpdateView):
    model = Status
    fields = ["name"]
    template_name = "status_form.html"
    success_url = reverse_lazy("status_list")


class StatusDeleteView(DeleteView):
    model = Status
    template_name = "status_confirm_delete.html"
    success_url = reverse_lazy("status_list")


########################################################################################################################
#                                                Type View's                                                           #
########################################################################################################################


class TypeListView(ListView):
    model = Type
    template_name = "type_list.html"
    context_object_name = "types"


class TypeDetailView(DetailView):
    model = Type
    template_name = "type_detail.html"
    context_object_name = "type"


class TypeCreateView(CreateView):
    model = Type
    fields = ["name"]
    template_name = "type_form.html"
    success_url = reverse_lazy("type_list")


class TypeUpdateView(UpdateView):
    model = Type
    fields = ["name"]
    template_name = "type_form.html"
    success_url = reverse_lazy("type_list")


class TypeDeleteView(DeleteView):
    model = Type
    template_name = "type_confirm_delete.html"
    success_url = reverse_lazy("type_list")


########################################################################################################################
#                                                Category View's                                                       #
########################################################################################################################


class CategoryListView(ListView):
    model = Category
    template_name = "category_list.html"
    context_object_name = "categories"


class CategoryDetailView(DetailView):
    model = Category
    template_name = "category_detail.html"
    context_object_name = "category"


class CategoryCreateView(CreateView):
    model = Category
    fields = ["name"]
    template_name = "category_form.html"
    success_url = reverse_lazy("category_list")


class CategoryUpdateView(UpdateView):
    model = Category
    fields = ["name"]
    template_name = "category_form.html"
    success_url = reverse_lazy("category_list")


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "category_confirm_delete.html"
    success_url = reverse_lazy("category_list")


########################################################################################################################
#                                                Subcategory View's                                                    #
########################################################################################################################


class SubcategoryListView(ListView):
    model = Subcategory
    template_name = "subcategory_list.html"
    context_object_name = "subcategories"


class SubcategoryDetailView(DetailView):
    model = Subcategory
    template_name = "subcategory_detail.html"
    context_object_name = "subcategory"


class SubcategoryCreateView(CreateView):
    model = Subcategory
    fields = ["name", "category"]
    template_name = "subcategory_form.html"
    success_url = reverse_lazy("subcategory_list")


class SubcategoryUpdateView(UpdateView):
    model = Subcategory
    fields = ["name", "category"]
    template_name = "subcategory_form.html"
    success_url = reverse_lazy("subcategory_list")


class SubcategoryDeleteView(DeleteView):
    model = Subcategory
    template_name = "subcategory_confirm_delete.html"
    success_url = reverse_lazy("subcategory_list")


def manage_all(request):
    # Получаем все записи
    statuses = Status.objects.all()
    types = Type.objects.all()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()

    # Инициализация переменных
    action = request.GET.get("action")
    model_name = request.GET.get("model")
    obj_id = request.GET.get("id")

    # Обработка добавления
    if request.method == "POST":
        if model_name == "status":
            form = StatusForm(request.POST)
        elif model_name == "type":
            form = TypeForm(request.POST)
        elif model_name == "category":
            form = CategoryForm(request.POST)
        elif model_name == "subcategory":
            form = SubcategoryForm(request.POST)
        else:
            form = None

        if form and form.is_valid():
            form.save()
            return redirect("manage_all")

    # Обработка редактирования
    if action == "edit" and obj_id:
        if model_name == "status":
            instance = get_object_or_404(Status, pk=obj_id)
            form_class = StatusForm
        elif model_name == "type":
            instance = get_object_or_404(Type, pk=obj_id)
            form_class = TypeForm
        elif model_name == "category":
            instance = get_object_or_404(Category, pk=obj_id)
            form_class = CategoryForm
        elif model_name == "subcategory":
            instance = get_object_or_404(Subcategory, pk=obj_id)
            form_class = SubcategoryForm
        else:
            instance = None
            form_class = None

        if request.method == "POST" and instance:
            form = form_class(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                return redirect("manage_all")
        else:
            form = form_class(instance=instance)

    # Обработка удаления
    if action == "delete" and obj_id:
        if model_name == "status":
            obj = get_object_or_404(Status, pk=obj_id)
        elif model_name == "type":
            obj = get_object_or_404(Type, pk=obj_id)
        elif model_name == "category":
            obj = get_object_or_404(Category, pk=obj_id)
        elif model_name == "subcategory":
            obj = get_object_or_404(Subcategory, pk=obj_id)
        else:
            obj = None

        if request.method == "POST" and obj:
            obj.delete()
            return redirect("manage_all")

    context = {
        "statuses": statuses,
        "types": types,
        "categories": categories,
        "subcategories": subcategories,
        "current_action": action,
        "current_model": model_name,
        "form": form if "form" in locals() else None,
        "edit_obj": obj if "obj" in locals() else None,
    }
    return render(request, "manage_all.html", context)
