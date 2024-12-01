from datetime import timedelta

from django.db import models


class Directory(models.Model):
    name = models.CharField(max_length=255)  # Название директории
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="subdirectories",
    )  # Рекурсивная связь с родительской директорией
    files = models.ManyToManyField(
        "File", blank=True, related_name="directories"
    )  # Множество файлов в директории

    def to_dict(self):
        # Преобразуем объект в словарь для отправки на фронт
        return {
            "name": self.name,
            "files": [file.to_dict() for file in self.files.all()],
            "subdirectories": [
                subdirectory.to_dict() for subdirectory in self.subdirectories.all()
            ],
        }

    def __str__(self):
        return self.name


class File(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("processed", "Processed"),
        ("failed", "Failed"),
    ]

    name = models.CharField(max_length=255)  # Название файла
    size = models.PositiveIntegerField()  # Размер файла в байтах
    description = models.TextField(blank=True, null=True)  # Описание файла
    processing_start = models.DateTimeField(null=True, blank=True)  # Начало обработки
    processing_end = models.DateTimeField(null=True, blank=True)  # Конец обработки
    processing_time = models.DurationField(null=True, blank=True)  # Время обработки
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="pending"
    )  # Статус обработки
    original_language = models.CharField(
        max_length=50, blank=True, null=True
    )  # Язык оригинала
    original_text = models.TextField(blank=True, null=True)  # Текст оригинала
    translated_text = models.TextField(blank=True, null=True)  # Текст на русском
    directory = models.ForeignKey(
        Directory,
        related_name="file_directory",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )  # Ссылка на директорию, к которой принадлежит файл

    def save(self, *args, **kwargs):
        # Вычисление времени обработки, если дата начала и окончания заданы
        if self.processing_start and self.processing_end:
            self.processing_time = self.processing_end - self.processing_start
        super().save(*args, **kwargs)

    def to_dict(self):
        # Преобразуем объект в словарь для отправки на фронт
        return {
            "name": self.name,
            "size": self.size,
            "description": self.description,
            "processing_start": self.processing_start,
            "processing_end": self.processing_end,
            "processing_time": (
                str(self.processing_time) if self.processing_time else None
            ),
            "status": self.status,
            "original_language": self.original_language,
            "original_text": self.original_text,
            "translated_text": self.translated_text,
        }

    def __str__(self):
        return self.name
