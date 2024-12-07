from loguru import logger


def initialize_app_settings(sender, **kwargs):
    """Проверяет и устанавливает настройки приложения."""
    from django.db import transaction

    from config.models import AppSetting

    logger.info("Инициализация настроек приложения.")
    try:
        with transaction.atomic():
            # безопасные запросы к БД
            AppSetting.objects.get_or_create(
                key="root_directory",
                defaults={
                    "value": "D:\\Project\\project_Python\\Whisper_test_folder\\"
                },
            )
            root_directory = AppSetting.objects.get(key="root_directory").value
            logger.info(
                f"Настройка 'root_directory = {root_directory} ' создана или уже существует."
            )
    except Exception as e:
        logger.error(f"Ошибка инициализации настроек: {e}")
