from typing import Any, Dict

from config.models import AppSetting
from django.db import transaction
from django.db.models import Model
from loguru import logger


def initialize_app_settings(sender: Model, **kwargs: Dict[str, Any]) -> None:
    """Проверяет и устанавливает настройки приложения."""
    logger.info("Инициализация настроек приложения.")
    try:
        with transaction.atomic():
            # Попытка получить или создать настройку 'root_directory'
            setting, created = AppSetting.objects.get_or_create(
                key="root_directory",
                defaults={
                    "value": "D:\\Project\\project_Python\\Whisper_test_folder\\"
                },
            )
            # Логирование результата
            if created:
                logger.info(
                    f"Настройка 'root_directory' успешно создана с значением: {setting.value}"
                )
            else:
                logger.info(
                    f"Настройка 'root_directory' уже существует с значением: {setting.value}"
                )
    except Exception as err:
        logger.error(f"Ошибка инициализации настроек: {err}")
