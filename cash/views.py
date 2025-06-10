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
from .forms import CashFlowForm, StatusForm, TypeForm, CategoryForm, SubcategoryForm, CashFlowUpdateForm
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
    form_class = CashFlowUpdateForm
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
    """
    StatusListView:
        - отображает список всех статусов
        - использует шаблон: ../templates/status/status_list.html
        - контекстное имя: 'statuses'
    """
    model = Status
    template_name = "../templates/status/status_list.html"
    context_object_name = "statuses"


class StatusDetailView(DetailView):
    """
    StatusDetailView:
        - отображает детали выбранного статуса
        - использует шаблон: ../templates/status/status_detail.html
        - контекстное имя: 'status'
    """
    model = Status
    template_name = "../templates/status/status_detail.html"
    context_object_name = "status"


class StatusCreateView(CreateView):
    """
    StatusCreateView:
        - позволяет создать новый статус
        - использует поле: 'name'
        - шаблон: ../templates/status/status_form.html
        - после успешного создания перенаправляет на: 'cashflow:manage'
    """
    model = Status
    fields = ["name"]
    template_name = "../templates/status/status_form.html"
    success_url = reverse_lazy("cashflow:manage")


class StatusUpdateView(UpdateView):
    """
    StatusUpdateView:
        - позволяет редактировать существующий статус
        - использует поле: 'name'
        - шаблон: ../templates/status/status_form.html
        - после успешного обновления перенаправляет на: 'cashflow:manage'
    """
    model = Status
    fields = ["name"]
    template_name = "../templates/status/status_form.html"
    success_url = reverse_lazy("cashflow:manage")


class StatusDeleteView(DeleteView):
    """
    StatusDeleteView:
        - позволяет удалить статус
        - использует шаблон: ../templates/status/status_confirm_delete.html
        - после удаления перенаправляет на: 'cashflow:manage'
    """
    model = Status
    template_name = "../templates/status/status_confirm_delete.html"
    success_url = reverse_lazy("cashflow:manage")



########################################################################################################################
#                                                Type View's                                                           #
########################################################################################################################


class TypeListView(ListView):
    """
    TypeListView:
        - отображает список всех типов
        - использует шаблон: ../templates/type/type_list.html
        - контекстное имя: 'types'
    """
    model = Type
    template_name = "../templates/type/type_list.html"
    context_object_name = "types"


class TypeDetailView(DetailView):
    """
    TypeDetailView:
        - отображает детали выбранного типа
        - использует шаблон: ../templates/type/type_detail.html
        - контекстное имя: 'type'
    """
    model = Type
    template_name = "../templates/type/type_detail.html"
    context_object_name = "type"


class TypeCreateView(CreateView):
    """
    TypeCreateView:
        - позволяет создать новый тип
        - использует поле: 'name'
        - шаблон: ../templates/type/type_form.html
        - после успешного создания перенаправляет на: 'cashflow:manage'
    """
    model = Type
    fields = ["name"]
    template_name = "../templates/type/type_form.html"
    success_url = reverse_lazy("cashflow:manage")


class TypeUpdateView(UpdateView):
    """
    TypeUpdateView:
        - позволяет редактировать существующий тип
        - использует поле: 'name'
        - шаблон: ../templates/type/type_form.html
        - после успешного обновления перенаправляет на: 'cashflow:manage'
    """
    model = Type
    fields = ["name"]
    template_name = "../templates/type/type_form.html"
    success_url = reverse_lazy("cashflow:manage")


class TypeDeleteView(DeleteView):
    """
    TypeDeleteView:
        - позволяет удалить тип
        - использует шаблон: ../templates/type/type_confirm_delete.html
        - после удаления перенаправляет на: 'cashflow:manage'
    """
    model = Type
    template_name = "../templates/type/type_confirm_delete.html"
    success_url = reverse_lazy("cashflow:manage")



########################################################################################################################
#                                                Category View's                                                       #
########################################################################################################################


class CategoryListView(ListView):
    """
    CategoryListView:
        - отображает список всех категорий
        - использует шаблон: ../templates/category/category_list.html
        - контекстное имя: 'categories'
    """
    model = Category
    template_name = "../templates/category/category_list.html"
    context_object_name = "categories"


class CategoryDetailView(DetailView):
    """
    CategoryDetailView:
        - отображает детали выбранной категории
        - использует шаблон: ../templates/category/category_detail.html
        - контекстное имя: 'category'
    """
    model = Category
    template_name = "../templates/category/category_detail.html"
    context_object_name = "category"


class CategoryCreateView(CreateView):
    """
    CategoryCreateView:
        - позволяет создать новую категорию
        - использует форму: CategoryForm
        - шаблон: ../templates/category/category_form.html
        - после успешного создания перенаправляет на: 'cashflow:manage'
    """
    model = Category
    form_class = CategoryForm
    template_name = "../templates/category/category_form.html"
    success_url = reverse_lazy("cashflow:manage")


class CategoryUpdateView(UpdateView):
    """
    CategoryUpdateView:
        - позволяет редактировать существующую категорию
        - использует форму: CategoryForm
        - шаблон: ../templates/category/category_form.html
        - после успешного обновления перенаправляет на: 'cashflow:manage'
    """
    model = Category
    form_class = CategoryForm
    template_name = "../templates/category/category_form.html"
    success_url = reverse_lazy("cashflow:manage")


class CategoryDeleteView(DeleteView):
    """
    CategoryDeleteView:
        - позволяет удалить категорию
        - использует шаблон: ../templates/category/category_confirm_delete.html
        - после удаления перенаправляет на: 'cashflow:manage'
    """
    model = Category
    template_name = "../templates/category/category_confirm_delete.html"
    success_url = reverse_lazy("cashflow:manage")



########################################################################################################################
#                                                Subcategory View's                                                    #
########################################################################################################################


class SubcategoryListView(ListView):
    """
    SubcategoryListView:
        - отображает список всех подкатегорий
        - использует шаблон: ../templates/subcategory/subcategory_list.html
        - контекстное имя: 'subcategories'
    """
    model = Subcategory
    template_name = "../templates/subcategory/subcategory_list.html"
    context_object_name = "subcategories"


class SubcategoryDetailView(DetailView):
    """
    SubcategoryDetailView:
        - отображает детали выбранной подкатегории
        - использует шаблон: ../templates/subcategory/subcategory_detail.html
        - контекстное имя: 'subcategory'
    """

    model = Subcategory
    template_name = "../templates/subcategory/subcategory_detail.html"
    context_object_name = "subcategory"


class SubcategoryCreateView(CreateView):
    """
    SubcategoryCreateView:
        - позволяет создать новую подкатегорию
        - использует форму: SubcategoryForm
        - шаблон: ../templates/subcategory/subcategory_form.html
        - после успешного создания перенаправляет на: 'cashflow:manage'
    """
    model = Subcategory
    form_class = SubcategoryForm
    template_name = "../templates/subcategory/subcategory_form.html"
    success_url = reverse_lazy("cashflow:manage")


class SubcategoryUpdateView(UpdateView):
    """
    SubcategoryUpdateView:
        - позволяет редактировать существующую подкатегорию
        - использует форму: SubcategoryForm
        - шаблон: ../templates/subcategory/subcategory_form.html
        - после успешного обновления перенаправляет на: 'cashflow:manage'
    """
    model = Subcategory
    form_class = SubcategoryForm
    template_name = "../templates/subcategory/subcategory_form.html"
    success_url = reverse_lazy("cashflow:manage")


class SubcategoryDeleteView(DeleteView):
    """
    SubcategoryDeleteView:
        - позволяет удалить подкатегорию
        - использует шаблон: ../templates/subcategory/subcategory_confirm_delete.html
        - после удаления перенаправляет на: 'cashflow:manage'
    """
    model = Subcategory
    template_name = "../templates/subcategory/subcategory_confirm_delete.html"
    success_url = reverse_lazy("cashflow:manage")


# Other views #


def manage_all(request):
    """
    🔧 Управление всеми сущностями: статусы, типы, категории и подкатегории

    Эта функция служит центральным хабом для просмотра, добавления, редактирования и удаления
    записей в моделях Status, Type, Category и Subcategory. Обеспечивает динамическое управление
    через универсальный интерфейс, основанный на параметрах GET и POST.

    Основные возможности:
    - Получение и отображение всех записей по моделям
    - Создание новых записей через формы
    - Редактирование существующих с предзаполненными формами
    - Удаление выбранных элементов с подтверждением

    Используемые параметры запроса:
    - `action`: действие ('edit', 'delete' или отсутствует для просмотра)
    - `model`: название модели ('status', 'type', 'category', 'subcategory')
    - `id`: идентификатор объекта для редактирования или удаления

    Важные моменты:
    - Автоматическая обработка форм в зависимости от модели
    - Перенаправление на страницу управления после успешных операций
    - Передача в шаблон всех данных для отображения и взаимодействия

    В результате — мощный и гибкий инструмент для администрирования всех связанных данных
    в одном месте, с минимальными усилиями и максимальной гибкостью.
    """
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

