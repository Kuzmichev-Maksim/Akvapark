import os
from datetime import datetime
from django.conf import settings

def log_action(message):
    log_file_path = os.path.join(settings.BASE_DIR, 'log.txt')
    
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(f"[{datetime.now()}] {message}\n")
        log_file.write("\n")