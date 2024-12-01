from django.db import models


class Setting(models.Model):
    key = models.CharField(max_length=255, unique=True)  # Уникальный ключ настройки
    value = models.TextField()  # Значение настройки, хранимое как строка
    description = models.TextField(
        blank=True, null=True
    )  # Описание настройки (необязательное)

    def get_value(self):
        """Возвращает значение поля `value` как строку."""
        return self.value

    def set_value(self, value):
        """Устанавливает значение поля `value` как строку."""
        self.value = str(value)  # Преобразует любое значение в строку

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = "Setting"
        verbose_name_plural = "Settings"
