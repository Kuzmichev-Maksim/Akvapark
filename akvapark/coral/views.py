import csv
from django.db import connection
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views import View
from .forms import ImportReceiptsForm, RegistrationForm, ZoneForm
from .models import Attraction, Logs, PaymentMethod, Receipt, ServiceType, Ticket, User, Role, ViewReceipts, ViewUsers, Zone
from django.db.models import Count
from django.core.management import call_command
from .utils import log_action


from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.contrib.auth.hashers import make_password  # Импортируем функцию для хеширования пароля
from .forms import RegistrationForm
from .models import Role
from .utils import log_action

def regis(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Получаем данные из формы
                last_name = form.cleaned_data['last_name']
                first_name = form.cleaned_data['first_name']
                middle_name = form.cleaned_data['middle_name']
                birth_date = form.cleaned_data['birth_date']
                login = form.cleaned_data['login']
                password = form.cleaned_data['password']
                role = form.cleaned_data.get('role', Role.objects.get(id=2))  # Получаем объект Role, а не id

                # Хешируем пароль
                hashed_password = make_password(password)  # Создаем хешированный пароль

                # Вызов процедуры register_user
                with connection.cursor() as cursor:
                    cursor.execute(
                        "CALL register_user(%s, %s, %s, %s, %s, %s, %s, %s);",
                        [
                            last_name,
                            first_name,
                            middle_name,
                            birth_date,
                            login,
                            hashed_password,  # Передаем хешированный пароль
                            role.id,
                            False  # Устанавливаем is_staff по умолчанию как False
                        ]
                    )

                # Логирование успешного действия
                log_action(f"Пользователь зарегистрирован: {login}")

                # Перенаправление на страницу входа
                return redirect('login')

            except Exception as e:
                # Обработка ошибки
                messages.error(request, 'Произошла ошибка при регистрации. Пожалуйста, попробуйте снова.')
                log_action(f"Ошибка регистрации: {e}")
        else:
            # Обработка ошибок валидации формы
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
            log_action(f"Ошибка регистрации: {form.errors}")
    else:
        form = RegistrationForm()

    return render(request, 'regis.html', {'form': form})

def start(request):
    log_action(f"Страница 'login.html' открыта пользователем: {request.user.login if request.user.is_authenticated else 'Гость'}")
    return render(request, 'login.html')


def attractions(request):
    log_action(f"Страница 'attractions.html' открыта пользователем: {request.user.login if request.user.is_authenticated else 'Гость'}")
    # Фильтруем аттракционы по зонам
    attractions = Attraction.objects.filter(zone_id=3)
    attractions_spa = Attraction.objects.filter(zone_id=4)
    attractions_kids = Attraction.objects.filter(zone_id=5)
    attractions_termy = Attraction.objects.filter(zone_id=6)

    return render(request, 'attractions.html', {
        'attractions': attractions,
        'attractions_spa': attractions_spa,
        'attractions_kids': attractions_kids,
        'attractions_termy': attractions_termy,
    })
    
def tariffs(request):
    log_action(f"Страница 'tariffs.html' открыта пользователем: {request.user.login if request.user.is_authenticated else 'Гость'}")
    return render(request, 'tariffs.html')


def account(request):
    log_action(f"Страница 'account.html' открыта пользователем")
    user = request.user
    tickets = Ticket.objects.filter(visitor=user)
    return render(request, 'account.html', {'user': user, 'tickets': tickets})

def tickets(request):
    log_action(f"Страница 'tickets.html' открыта пользователем: {request.user.login if request.user.is_authenticated else 'Гость'}")
    services = ServiceType.objects.all()
    return render(request, 'tickets.html', {'services': services})

def home(request):
    log_action(f"Страница 'home.html' открыта пользователем: {request.user.login if request.user.is_authenticated else 'Гость'}")
    return render(request, 'home.html')


def add_review(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        return redirect('account')  # Перенаправление после успешного сохранения
    return HttpResponse("Неверный метод запроса", status=405)


def login_view(request):
    if request.method == 'POST':
        login_value = request.POST.get('login')  # Логин пользователя
        password = request.POST.get('password')  # Пароль пользователя

        # Аутентификация пользователя с использованием логина
        user = authenticate(request, username=login_value, password=password)

        if user is not None:
            login(request, user)

           
            # Проверка роли для перенаправления на кастомные страницы
            if user.role.name == 'ADMIN':  # Если роль администратора
                return redirect('manage')  # Перенаправление на кастомную страницу администратора
            else:

                log_action(f"Пользователь {user.login} успешно вошел в систему")
                return redirect('home')  # Обычные пользователи перенаправляются на главную страницу
        else:
            messages.error(request, 'Неверный логин или пароль')
            log_action(f"Ошибка входа: неверный логин или пароль")

    return render(request, 'login.html')

def manage(request):
    zones = Zone.objects.all()
    attractions = Attraction.objects.all()

    if request.method == "POST":
        # Логируем открытие страницы управления
        log_action(f"Страница управления открыта пользователем: {request.user.login if request.user.is_authenticated else 'Гость'}")

        # Обновление зоны
        if "update_zone" in request.POST:
            zone_id = request.POST["update_zone"]
            zone = Zone.objects.get(pk=zone_id)
            zone.name = request.POST.get(f"zone_name_{zone_id}")
            zone.save()
            # Вызов функции log_action в PostgreSQL
            with connection.cursor() as cursor:
                cursor.execute("SELECT log_action(%s);", [f"Зона обновлена: ID {zone_id}, новое имя: {zone.name}"])

            log_action(f"Зона обновлена: ID {zone_id}, новое имя: {zone.name}")

        # Удаление зоны
        elif "delete_zone" in request.POST:
            zone_id = request.POST["delete_zone"]
            try:
                zone = Zone.objects.get(pk=zone_id)
                zone.delete()
                log_action(f"Зона удалена: ID {zone_id}, имя: {zone.name}")
                with connection.cursor() as cursor:
                    cursor.execute("SELECT log_action(%s);", [f"Зона удалена: ID {zone_id}, имя: {zone.name}"])

            except Zone.DoesNotExist:
                log_action(f"Ошибка: Зона с ID {zone_id} не найдена")
                

        # Добавление новой зоны
        elif "add_zone" in request.POST:
            new_zone_name = request.POST.get("new_zone_name")
            if new_zone_name:
                zone = Zone.objects.create(name=new_zone_name)
                log_action(f"Новая зона добавлена: ID {zone.id}, имя: {zone.name}")
                with connection.cursor() as cursor:
                    cursor.execute("SELECT log_action(%s);", [f"Новая зона добавлена: ID {zone_id}, имя: {zone.name}"])


        # Обновление аттракциона
        elif "update_attraction" in request.POST:
            attraction_id = request.POST["update_attraction"]
            try:
                attraction = Attraction.objects.get(pk=attraction_id)
                attraction.name = request.POST.get(f"attraction_name_{attraction_id}")
                attraction.description = request.POST.get(f"attraction_description_{attraction_id}")
                zone_id = request.POST.get(f"attraction_zone_{attraction_id}")
                attraction.zone = Zone.objects.get(pk=zone_id)
                attraction.image_url = request.POST.get(f"attraction_image_url_{attraction_id}")
                attraction.save()
                log_action(f"Аттракцион обновлен: ID {attraction_id}, новое имя: {attraction.name}")
                with connection.cursor() as cursor:
                    cursor.execute("SELECT log_action(%s);", [f"Аттракцион обновлен: ID {attraction}"])

            except Attraction.DoesNotExist:
                log_action(f"Ошибка: Аттракцион с ID {attraction_id} не найден")

        # Удаление аттракциона
        elif "delete_attraction" in request.POST:
            attraction_id = request.POST["delete_attraction"]
            try:
                attraction = Attraction.objects.get(pk=attraction_id)
                attraction.delete()
                log_action(f"Аттракцион удален: ID {attraction_id}, имя: {attraction.name}")
                with connection.cursor() as cursor:
                    cursor.execute("SELECT log_action(%s);", [f"Аттракцион удален: ID {attraction}, имя: {attraction.name}"])

            except Attraction.DoesNotExist:
                log_action(f"Ошибка: Аттракцион с ID {attraction_id} не найден")

        # Добавление нового аттракциона
        elif "add_attraction" in request.POST:
            new_name = request.POST.get("new_attraction_name")
            new_description = request.POST.get("new_attraction_description")
            zone_id = request.POST.get("new_attraction_zone")
            new_image_url = request.POST.get("new_attraction_image_url")  # Получаем URL картинки
            if new_name and new_description and zone_id:
                attraction = Attraction.objects.create(
                    name=new_name,
                    description=new_description,
                    zone=Zone.objects.get(pk=zone_id),
                    image_url=new_image_url  # Сохраняем URL картинки
                )
                log_action(f"Новый аттракцион добавлен: ID {attraction.id}, имя: {attraction.name}")
                with connection.cursor() as cursor:
                    cursor.execute("SELECT log_action(%s);", [f"Новый аттракцион добавлен: ID {attraction}, имя: {attraction.name}"])


        return redirect("manage")  # Перезагрузка страницы для обновления данных

    return render(request, "admin.html", {"zones": zones, "attractions": attractions})


def process_payment(request):
    if request.method == 'POST':
        # Получаем данные из формы
        total_amount = request.POST.get('totalAmount')
        adult_quantity = request.POST.get('adultQuantity')
        child_quantity = request.POST.get('childQuantity')
        baby_quantity = request.POST.get('babyQuantity')
        service_id = request.POST.get('serviceId')
        visit_date = request.POST.get('visitDate')  # Предполагается, что дата посещения передается

        # Получаем текущего пользователя (предполагается, что пользователь авторизован)
        user = request.user

        # Получаем тип услуги
        service_type = get_object_or_404(ServiceType, id=service_id)

        # Создаем билет
        ticket = Ticket.objects.create(
            price=total_amount,
            visit_date=visit_date,
            quantity=int(adult_quantity) + int(child_quantity) + int(baby_quantity),
            visitor=user,
            service_type=service_type
        )

        log_action(f"Билет создан: ID {ticket.id}, пользователь: {user.login}, сумма: {total_amount}, дата посещения: {visit_date}")
        with connection.cursor() as cursor:
                    cursor.execute("SELECT log_action(%s);", [f"Билет создан: ID {ticket.id}, пользователь: {user.login}, сумма: {total_amount}, дата посещения: {visit_date}"])

        payment_method = get_object_or_404(PaymentMethod, id=1)

        # Создаем чек
        receipt = Receipt.objects.create(
            amount=total_amount,
            payment_method=payment_method,
            ticket=ticket
        )

        log_action(f"Чек создан: ID {receipt.id}, билет: {ticket.id}, сумма: {total_amount}, метод оплаты: {payment_method.name}")
        with connection.cursor() as cursor:
                    cursor.execute("SELECT log_action(%s);", [f"Чек создан: ID {receipt.id}, билет: {ticket.id}, сумма: {total_amount}, метод оплаты: {payment_method.name}"])

        # Возвращаем успешный ответ
        return JsonResponse({'status': 'success', 'message': 'Билет успешно куплен и чек создан'})

    return JsonResponse({'status': 'error', 'message': 'Неверный метод запроса'})

def statistics(request):
    log_action(f"Страница 'statistics.html' открыта пользователем: {request.user.login if request.user.is_authenticated else 'Гость'}")
    # Статистика по типу услуги
    ticket_stats = Ticket.objects.values('service_type__name').annotate(count=Count('id'))
    service_types = [stat['service_type__name'] for stat in ticket_stats]
    ticket_counts = [stat['count'] for stat in ticket_stats]

    # Статистика по дате посещения
    visit_stats = Ticket.objects.values('visit_date').annotate(count=Count('id'))
    visit_dates = [stat['visit_date'].strftime('%d.%m.%Y') for stat in visit_stats]  # Формат: день-месяц-год
    visit_counts = [stat['count'] for stat in visit_stats]

    return render(request, 'statistics.html', {
        'service_types': service_types,
        'ticket_counts': ticket_counts,
        'visit_dates': visit_dates,
        'visit_counts': visit_counts,
    })


     
def checks(request):
    log_action(f"Страница 'checks.html' открыта пользователем: {request.user.login if request.user.is_authenticated else 'Гость'}")
    form = ImportReceiptsForm() 
    receipts = ViewReceipts.objects.all()
    return render(request, 'checks.html',  {'form': form, 'receipts': receipts})


def users(request):
    log_action(f"Страница 'users.html' открыта пользователем: {request.user.login if request.user.is_authenticated else 'Гость'}")
    users = ViewUsers.objects.all()
    return render(request, 'users.html', {'users': users})

def logs(request):
    logs = Logs.objects.all().order_by('-created_at')  
    log_action(f"Страница 'logs.html' открыта пользователем: {request.user.login if request.user.is_authenticated else 'Гость'}")
    return render(request, 'logs.html', {'logs': logs}) 


def backup_db_view(request):
    if request.method == 'POST':
        try:
            call_command('backup_db')
        except Exception as e:
            return HttpResponse(f'Ошибка при создании бекапа: {e}')
    return render(request, 'admin.html')



# class ExportReceiptsView(View):
#     def get(self, request, *args, **kwargs):
#         response = HttpResponse(content_type='text/csv; charset=utf-8')  # Указываем кодировку
#         response['Content-Disposition'] = 'attachment; filename="receipts.csv"'

#         writer = csv.writer(response)
#         writer.writerow(['ID', 'Сумма', 'Дата оплаты', 'Способ оплаты', 'Услуги'])

#         receipts = Receipt.objects.all().select_related('payment_method', 'ticket__service_type')
#         for receipt in receipts:
#             writer.writerow([
#                 receipt.id,
#                 receipt.amount,
#                 receipt.payment_date,
#                 receipt.payment_method.name,
#                 receipt.ticket.service_type.name,
#             ])
        
#         log_action(f"CSV файл с чеками был сохранен")
#         return response
    

# class ImportReceiptsView(View):
#     def get(self, request, *args, **kwargs):
#         form = ImportReceiptsForm()
#         return render(request, 'checks.html', {'form': form})

#     def post(self, request, *args, **kwargs):
#         form = ImportReceiptsForm(request.POST, request.FILES)
#         if form.is_valid():
#             file = form.cleaned_data['file']

#             # Проверяем, что файл существует
#             if not file:
#                 return render(request, 'checks.html', {'form': form, 'error': 'Файл не выбран'})

#             try:
#                 # Читаем файл и декодируем его
#                 decoded_file = file.read().decode('utf-8').splitlines()
#                 reader = csv.DictReader(decoded_file)

#                 # Обрабатываем каждую строку CSV
#                 for row in reader:
#                     try:
#                         # Пробуем найти существующую запись по идентификатору
#                         receipt = Receipt.objects.filter(id=row['ID']).first()

#                         if receipt:
#                             # Обновляем существующую запись
#                             receipt.amount = row['Сумма']
#                             receipt.payment_date = row['Дата оплаты']
#                             receipt.payment_method = PaymentMethod.objects.get(name=row['Способ оплаты'])
#                             receipt.ticket = Ticket.objects.get(name=row['Услуги'])
#                             receipt.save()
#                         else:
#                             # Создаем новую запись, если её нет
#                             Receipt.objects.create(
#                                 amount=row['Сумма'],
#                                 payment_date=row['Дата оплаты'],
#                                 payment_method=PaymentMethod.objects.get(name=row['Способ оплаты']),
#                                 ticket=Ticket.objects.get(name=row['Услуги']),
#                             )
#                     except Exception as e:
#                         # Обрабатываем ошибки при обработке строки
#                         return render(request, 'checks.html', {'form': form, 'error': f'Ошибка при обработке строки: {e}'})

#                 # Перенаправляем на страницу успеха
#                 return redirect('checks')

#             except Exception as e:
#                 # Обрабатываем ошибки при чтении файла
#                 return render(request, 'checks.html', {'form': form, 'error': f'Ошибка при чтении файла: {e}'})

#         return render(request, 'checks.html', {'form': form})