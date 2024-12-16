from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError("Login is required")
        user = self.model(login=login, **extra_fields)
        user.set_password(password)  # Хэшируем пароль
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('role_id', 1)  # Устанавливаем роль как 'ADMIN'
        return self.create_user(login, password, **extra_fields)


class User(AbstractBaseUser):
    last_name = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    birth_date = models.DateField()
    login = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    role = models.ForeignKey('Role', on_delete=models.CASCADE, related_name='users')
    is_staff = models.BooleanField(default=False)

    last_login = None

    objects = UserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['last_name', 'first_name', 'birth_date', 'role']

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.login})"

    # Добавляем необходимые методы для работы с правами
    def has_perm(self, perm, obj=None):
        return self.is_staff  # Все администраторы могут иметь все права

    def has_module_perms(self, app_label):
        return self.is_staff  # Проверка на доступ к модулю

    def get_all_permissions(self):
        if self.is_staff:
            return ['admin']  # Список всех прав для администраторов
        return []