import sys

from django.apps import AppConfig

# from django.db.models.signals import post_migrate
from loguru import logger


class FilesConfig(AppConfig):
    name = "files"

    def ready(self) -> None:
        from config.models import AppSetting

        from .config_operations import initialize_app_settings
        from .db_operations import main_db_operations
        from .file_operations import sync_database_with_directory

        logger.debug("FilesConfig: вызван метод ready()")
        # Только для команды runserver
        if "runserver" in sys.argv:
            # Создаем базу данных и применяем миграции
            main_db_operations()
            # Проверяем и устанавливаем настройки приложения.
            initialize_app_settings(sender=self)
            # Синхронизируем структуру директории с базой данных.
            root_directory = AppSetting.objects.get(key="root_directory").value
            sync_database_with_directory(root_path=root_directory)
