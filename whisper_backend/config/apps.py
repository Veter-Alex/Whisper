from django.apps import AppConfig
from loguru import logger


class ConfigAppConfig(AppConfig):
    name = "config"

    def ready(self):
        """Подключение сигналов после загрузки приложения."""
        from .signals import initialize_app_settings  # Импортируем сигнал

        logger.info("ConfigAppConfig: вызван метод ready()")

        # post_migrate.connect(set_default_settings, sender=self)
        initialize_app_settings(sender=self)
