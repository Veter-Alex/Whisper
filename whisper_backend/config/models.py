from typing import Optional, Union

from django.db import connection, models


class AppSetting(models.Model):
    """Модель для хранения пользовательских настроек приложения."""

    key = models.CharField(max_length=255, unique=True)  # Название настройки
    value = models.TextField()  # Значение настройки
    description = models.TextField(
        blank=True, null=True
    )  # Описание настройки (опционально)

    def __str__(self) -> str:
        return f"{self.key}: {self.value}"

    @classmethod
    def get_setting(cls, key: str) -> Optional[str]:
        """
        Получение значения настройки по ключу.
        Возвращает значение настройки или None, если настройка не найдена.
        """
        try:
            setting = cls.objects.get(key=key)
            return setting.value
        except cls.DoesNotExist:
            return None

    @classmethod
    def set_setting(
        cls, key: str, value: Union[str, int, float]
    ) -> "AppSetting":
        """
        Установка значения настройки по ключу.
        Возвращает объект настройки.
        """
        setting, created = cls.objects.update_or_create(
            key=key, defaults={"value": value}
        )
        return setting

    @classmethod
    def table_exists(cls) -> bool:
        """
        Проверяет, существует ли таблица модели в базе данных.
        Возвращает True, если таблица существует, иначе False.
        """
        return cls._meta.db_table in connection.introspection.table_names()
