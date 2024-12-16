from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib import messages
from .forms import RegistrationForm
from .models import User, Role


def regis(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем пользователя в базе данных
            messages.success(request, 'Вы успешно зарегистрированы!')
            return redirect('login')  # Перенаправляем на страницу входа
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = RegistrationForm()

    return render(request, 'regis.html', {'form': form})


def start(request):
    return render(request, 'login.html')


def attractions(request):
    return render(request, 'attractions.html')


def tariffs(request):
    return render(request, 'tariffs.html')


def account(request):
    return render(request, 'account.html')


def tickets(request):
    return render(request, 'tickets.html')


def home(request):
    return render(request, 'home.html')

def admin(request):
    return render(request, 'admin.html')


def add_review(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        # Предполагается наличие модели Review
        # Review.objects.create(rating=rating, comment=comment, user=request.user)
        return redirect('account')  # Перенаправление после успешного сохранения
    return HttpResponse("Неверный метод запроса", status=405)


def login_view(request):
    if request.method == 'POST':
        login_value = request.POST.get('login')  # Логин пользователя
        password = request.POST.get('password')  # Пароль пользователя

        # Используем login вместо username в authenticate()
        user = authenticate(request, username=login_value, password=password)

        if user is not None:
            login(request, user)  # Авторизуем пользователя

            # Проверка роли пользователя
            if user.role.name == 'ADMIN':  # Если роль ADMIN
                return redirect('admin')  # Перенаправляем на страницу администратора

            return redirect('home')  # Перенаправляем на главную страницу, если не ADMIN
        else:
            messages.error(request, 'Неверный логин или пароль')

    return render(request, 'login.html')  # Рендерим шаблон для GET-запросов