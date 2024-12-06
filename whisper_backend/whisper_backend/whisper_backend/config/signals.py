# signals.py
from loguru import logger


def initialize_app_settings(sender, **kwargs):
    """Устанавливает настройки приложения после миграций."""
    from django.db import transaction

    from .models import AppSetting  # Импортируем только внутри функции

    logger.info("Инициализация настроек приложения.")
    try:
        with transaction.atomic():
            # Здесь только безопасные запросы к БД
            AppSetting.objects.get_or_create(
                key="root_directory", defaults={"value": ""}
            )
            logger.info("Настройка 'root_directory' создана или уже существует.")
    except Exception as e:
        logger.error(f"Ошибка инициализации настроек: {e}")
