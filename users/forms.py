from django.contrib.auth.forms import UserCreationForm
from users.models import User
from django import forms


class UserRegisterForm(UserCreationForm):
    """
    Форма регистрации пользователя.
    """
    class Meta:
        model = User
        fields = ("email", "phone", "password1", "password2")

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры.")
        return phone_number

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите электронную почту"}
        )
        self.fields["phone"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите номер телефона"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите пароль"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите тот же пароль"}
        )
