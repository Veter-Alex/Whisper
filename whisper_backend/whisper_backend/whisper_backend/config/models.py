from django.db import connection, models


class AppSetting(models.Model):
    """Модель для хранения пользовательских настроек приложения."""

    key = models.CharField(max_length=255, unique=True)  # Название настройки
    value = models.TextField()  # Значение настройки
    description = models.TextField(
        blank=True, null=True
    )  # Описание настройки (опционально)

    def __str__(self):
        return f"{self.key}: {self.value}"

    @classmethod
    def get_setting(cls, key):
        """Получение значения настройки по ключу."""
        try:
            setting = cls.objects.get(key=key)
            return setting.value
        except cls.DoesNotExist:
            return None

    @classmethod
    def set_setting(cls, key, value):
        """Установка значения настройки по ключу."""
        setting, created = cls.objects.update_or_create(
            key=key, defaults={"value": value}
        )
        return setting

    @classmethod
    def table_exists(cls):
        """Проверяет, существует ли таблица модели в базе данных."""
        return cls._meta.db_table in connection.introspection.table_names()
