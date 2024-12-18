import os
import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime

class Command(BaseCommand):
    help = 'Создает бекап базы данных'

    def handle(self, *args, **kwargs):
        # Путь к папке для хранения бекапов
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)

        # Имя файла бекапа
        backup_file = os.path.join(backup_dir, f'backup_{self.get_timestamp()}.sql')

        # Путь к файлу логов
        log_file_path = os.path.join(backup_dir, 'log.txt')

        # Команда для создания бекапа (для PostgreSQL)
        db_settings = settings.DATABASES['default']
        db_name = db_settings['NAME']
        db_user = db_settings['USER']
        db_password = db_settings['PASSWORD']
        db_host = db_settings['HOST']
        db_port = db_settings['PORT']

        # Полный путь к pg_dump.exe
        pg_dump_path = r"C:\Program Files\PostgreSQL\16\bin\pg_dump.exe"

        # Команда pg_dump для создания бекапа
        command = [
            pg_dump_path,  # Указываем полный путь к pg_dump
            '-U', db_user,
            '-h', db_host,
            '-p', db_port,
            '-F', 'c',
            '-b',
            '-v',
            '-f', backup_file,
            db_name
        ]

        # Устанавливаем пароль для подключения
        os.environ['PGPASSWORD'] = db_password

        try:
            self.stdout.write(self.style.SUCCESS('Создание бекапа...'))

            # Выполняем команду pg_dump
            result = subprocess.run(command, check=True, capture_output=True, text=True)

            # Записываем успешный вывод в лог
            with open(log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(f"[{datetime.now()}] Бекап создан: {backup_file}\n")
                log_file.write(result.stdout + '\n')

            self.stdout.write(self.style.SUCCESS(f'Бекап создан: {backup_file}'))
            self.stdout.write(result.stdout)  # Вывод команды

        except subprocess.CalledProcessError as e:
            # Записываем ошибку в лог
            with open(log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(f"[{datetime.now()}] Ошибка при создании бекапа: {e}\n")
                log_file.write(e.stderr + '\n')

            self.stdout.write(self.style.ERROR(f'Ошибка при создании бекапа: {e}'))
            self.stdout.write(e.stderr)  # Вывод ошибки

        finally:
            # Удаляем пароль из окружения
            del os.environ['PGPASSWORD']

    def get_timestamp(self):
        """Возвращает текущую дату и время в формате DD.MM.YYYY_HHMMSS"""
        return datetime.now().strftime('%d.%m.%Y_%H%M%S')