from django.core.management.base import BaseCommand
from users.models import User  # Импортируйте вашу модель


class Command(BaseCommand):
    help = "Добавляет данные в таблицу MyModel"

    def handle(self, *args, **kwargs):
        # Пример добавления одного объекта
        my_instance = User(
            email="test5@gmail.com",
            is_active=True,
            password="1234",
            tg_id="5152132161",
        )
        my_instance.save()
        self.stdout.write(self.style.SUCCESS("Данные успешно добавлены!"))
