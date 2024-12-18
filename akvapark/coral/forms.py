from django import forms
from .models import Attraction, User, Zone
from django.forms.widgets import DateInput

from django import forms
from django.core.exceptions import ValidationError
import re

from django import forms
from django.core.exceptions import ValidationError
import re

class RegistrationForm(forms.Form):
    last_name = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    middle_name = forms.CharField(max_length=150, required=False)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    login = forms.EmailField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if len(last_name) < 3:
            raise ValidationError("Фамилия должна содержать минимум 3 символа.")
        if not re.match(r'^[А-Яа-яЁё]+$', last_name):  # Проверка на только русские буквы
            raise ValidationError("Фамилия должна содержать только русские буквы.")
        return last_name

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if len(first_name) < 3:
            raise ValidationError("Имя должно содержать минимум 3 символа.")
        if not re.match(r'^[А-Яа-яЁё]+$', first_name):  # Проверка на только русские буквы
            raise ValidationError("Имя должно содержать только русские буквы.")
        return first_name

    def clean_middle_name(self):
        middle_name = self.cleaned_data.get('middle_name')
        if middle_name and len(middle_name) < 3:
            raise ValidationError("Отчество должно содержать минимум 3 символа.")
        if middle_name and not re.match(r'^[А-Яа-яЁё]+$', middle_name):  # Проверка на только русские буквы
            raise ValidationError("Отчество должно содержать только русские буквы.")
        return middle_name

    def clean_login(self):
        login = self.cleaned_data.get('login')
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', login):  # Проверка на формат email
            raise ValidationError("Неверный формат почты.")
        return login

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError("Пароль должен содержать минимум 8 символов.")
        if not any(char.islower() for char in password):
            raise ValidationError("Пароль должен содержать хотя бы одну строчную букву.")
        if not any(char.isupper() for char in password):
            raise ValidationError("Пароль должен содержать хотя бы одну заглавную букву.")
        if not any(char in '!@#$%^&*()-_=+<>?/' for char in password):
            raise ValidationError("Пароль должен содержать хотя бы один специальный символ.")
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError("Пароли не совпадают.")
        return confirm_password

class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = ['name']

class AttractionForm(forms.ModelForm):
    class Meta:
        model = Attraction
        fields = ['name', 'description', 'image_url', 'zone']

class ImportReceiptsForm(forms.Form):
    file = forms.FileField(label="Выберите CSV-файл")