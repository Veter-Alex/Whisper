from django.apps import AppConfig

# from django.db.models.signals import post_migrate
from loguru import logger
import sys


class FilesConfig(AppConfig):
    name = "files"

    def ready(self):
        from config.models import AppSetting
        from .db_operations import create_database
        from .config_operations import initialize_app_settings
        from .file_operations import sync_database_with_directory

        logger.debug("FilesConfig: вызван метод ready()")
        # Только для команды runserver
        if "runserver" in sys.argv:
            # Создаем базу данных и применяем миграции
            create_database()
            # Проверяем и устанавливаем настройки приложения.
            initialize_app_settings(sender=self)
            # Синхронизируем структуру директории с базой данных.
            root_directory = AppSetting.objects.get(key="root_directory").value
            sync_database_with_directory(root_path=root_directory)
