from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Представление для страницы администратора
@login_required
def admin_view(request):
    if not request.user.is_staff:  # Проверка, является ли пользователь администратором
        messages.error(request, 'Доступ запрещён: недостаточно прав')
        return redirect('home')  # Перенаправляем на главную страницу
    return render(request, 'admin.html')  # Рендерим кастомную страницу админа