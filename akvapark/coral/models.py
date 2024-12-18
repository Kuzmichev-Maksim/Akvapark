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
    
    from django.db import models

# Модель Zone (Зона)
class Zone(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название зоны")

    def __str__(self):
        return self.name


# Модель Attraction (Аттракцион)
class Attraction(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название аттракциона")
    description = models.TextField(verbose_name="Описание")
    image_url = models.URLField(max_length=200, verbose_name="Ссылка на изображение", blank=True, null=True)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, verbose_name="Зона", related_name="attractions")

    def __str__(self):
        return self.name
    
    
# Модель Ticket (Билет) 
class Ticket(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата покупки")  # Автоматически добавляется при создании
    visit_date = models.DateField(verbose_name="Дата посещения")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    # Внешний ключ на пользователя (посетителя)
    visitor = models.ForeignKey(
        'User',  # Ссылается на модель пользователя
        on_delete=models.CASCADE,
        related_name='tickets',
        verbose_name="Посетитель"
    )

    # Внешний ключ на тип услуги
    service_type = models.ForeignKey(
        'ServiceType',  # Ссылается на модель типа услуги
        on_delete=models.CASCADE,
        related_name='tickets',
        verbose_name="Тип услуги"
    )

    class Meta:
        verbose_name = "Билет"
        verbose_name_plural = "Билеты"
        ordering = ['-purchase_date']  # Сортировка по дате покупки в обратном порядке

    def __str__(self):
        return f"Билет ({self.service_type.name}) для {self.visitor.first_name} {self.visitor.last_name} на {self.visit_date}"

class ServiceType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название услуги")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена услуги")

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"
    

class PaymentMethod(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название способа оплаты")

    class Meta:
        verbose_name = "Способ оплаты"
        verbose_name_plural = "Способы оплаты"

    def __str__(self):
        return self.name
    

class Receipt(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    payment_method = models.ForeignKey(
        'PaymentMethod',  # Ссылается на модель способа оплаты
        on_delete=models.PROTECT,  # Защита от удаления способа оплаты, если он используется
        related_name='receipts',
        verbose_name="Способ оплаты"
    )
    ticket = models.ForeignKey(
        'Ticket',  # Ссылается на модель билета
        on_delete=models.CASCADE,  # Удаляет чек, если билет удален
        related_name='receipts',
        verbose_name="Билет"
    )

    class Meta:
        verbose_name = "Чек"
        verbose_name_plural = "Чеки"
        ordering = ['-payment_date']  # Сортировка по дате оплаты в обратном порядке

    def __str__(self):
        return f"Чек на {self.amount} руб. за билет {self.ticket.service_type.name} от {self.payment_date}"
    
class ViewReceipts(models.Model):
    receipt_id = models.IntegerField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    payment_method_name = models.CharField(max_length=255)
    service_type_name = models.CharField(max_length=255)
    # ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    # ticket_date = models.DateField()
    # visitor_name = models.CharField(max_length=255)

    class Meta:
        managed = False  # Указываем, что эта модель не управляется Django
        db_table = 'view_receipts'  # Имя представления в базе данных

    def __str__(self):
        return f"Чек на {self.amount} руб. за {self.service_type_name} от {self.payment_date}"
    
class ViewUsers(models.Model):
    user_id = models.IntegerField(primary_key=True)
    last_name = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    birth_date = models.DateField()
    login = models.CharField(max_length=150)
    role_name = models.CharField(max_length=100)

    class Meta:
        managed = False  # Указываем, что эта модель не управляется Django
        db_table = 'view_users'  # Имя представления в базе данных

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.login})"  
    

class Logs(models.Model):
    action = models.TextField(verbose_name="Действие")  # Поле для текста лога
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время")  # Автоматически заполняется текущей датой и временем

    class Meta:
        verbose_name = "Лог"
        verbose_name_plural = "Логи"
        ordering = ["-created_at"]  

    def __str__(self):
        return f"Лог от {self.created_at}: {self.action[:50]}"  # Отображение первых 50 символов действия