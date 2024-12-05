from django.db import models


class AppSetting(models.Model):
    # Название настройки (ключ)
    key = models.CharField(max_length=255, unique=True)

    # Значение настройки (например, строка, число, JSON и т. д.)
    value = models.TextField()

    # Описание настройки (необязательно)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.key}: {self.value}"

    @classmethod
    def get_setting(cls, key):
        """Метод для получения значения настройки по ключу."""
        try:
            setting = cls.objects.get(key=key)
            return setting.value
        except cls.DoesNotExist:
            return None

    @classmethod
    def set_setting(cls, key, value):
        """Метод для установки значения настройки по ключу."""
        setting, created = cls.objects.update_or_create(
            key=key, defaults={"value": value}
        )
        return setting
