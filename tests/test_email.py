import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(BASE_DIR / "src"))

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

import django

django.setup()

from django.conf import settings
from django.core.mail import send_mail


send_mail(
    subject="Тестовое",
    message="тестовое письмо",
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=["danielmaniel80@gmail.com",],
    fail_silently=False,
)

print("Письмо успешно отправлено")