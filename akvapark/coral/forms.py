from django import forms
from .models import User
from django.forms.widgets import DateInput

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    birth_date = forms.DateField(
        widget=DateInput(attrs={'type': 'date'})  # HTML5 виджет выбора даты
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'birth_date', 'login']

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        # Устанавливаем роль и is_staff, если это нужно
        if user.role.name == 'ADMIN':
            user.is_staff = True  # Сделать пользователя администратором
        else:
            user.is_staff = False  # Для обычных пользователей

        if commit:
            user.save()
        return user
