from django.apps import AppConfig
from django.db.models.signals import post_migrate
from loguru import logger


class FilesConfig(AppConfig):
    name = "files"

    def ready(self):
        from config.models import AppSetting

        from .file_operations import sync_database_with_directory

        logger.info("FilesConfig: вызван метод ready()")

        logger.info("Выполнение sync_database_with_directory после миграции")
        root_directory = AppSetting.objects.get(key="root_directory").value

        # Создаем обработчик сигнала, который вызывает sync_database_with_directory
        def sync_with_directory(sender, **kwargs):
            sync_database_with_directory(root_path=root_directory)

        # Подключаем обработчик к сигналу post_migrate
        sync_with_directory(sender=self)
