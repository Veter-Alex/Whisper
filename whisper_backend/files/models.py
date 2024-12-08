import os
from typing import Any, Optional

from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from loguru import logger


# Модель для хранения директорий
class Directory(models.Model):
    name = models.CharField(
        max_length=255, verbose_name="Имя директории"
    )  # Имя директории
    parent = models.ForeignKey(
        "self",  # Ссылка на саму себя для построения иерархии
        on_delete=models.CASCADE,  # При удалении родителя удаляются и все его дочерние директории
        null=True,  # Корневые директории могут не иметь родителя
        blank=True,  # Корневые директории могут быть пустыми
        db_index=True,  # Это необязательно, так как ForeignKey уже индексируется автоматически
        related_name="subdirectories",  # Имя для доступа к дочерним директориям через родителя
        verbose_name="Родительская директория",  # Имя родительской директории
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )  # Дата создания директории

    class Meta:
        indexes = [
            models.Index(
                fields=["parent"]
            ),  # Индекс для поля "parent" (для построения иерархии)
        ]
        unique_together = (
            "name",
            "parent",
        )  # Имя директории уникально в пределах одного родителя

    def __str__(self) -> str:
        # При выводе объекта в строковом формате будем показывать родителя, если он есть
        return f"{self.name} (Parent: {self.parent.name if self.parent else 'None'})"

    @classmethod
    def add_directory(
        cls, name: str, parent: Optional["Directory"] = None
    ) -> "Directory":
        """
        Метод для добавления новой директории.
        """
        directory = cls.objects.create(name=name, parent=parent)
        return directory

    @transaction.atomic
    def delete_directory(self) -> None:
        """
        Метод для удаления текущей директории, включая все дочерние директории и файлы.
        """
        try:
            self.delete()
        except ObjectDoesNotExist:
            pass


# Модель для хранения файлов
class File(models.Model):
    STATUS_CHOICES = [
        ("in_queue", "В очереди"),
        ("in_progress", "В процессе обработки"),
        ("completed", "Обработка завершена"),
        ("error", "Ошибка обработки"),
    ]

    name = models.CharField(max_length=255, verbose_name="Имя файла")
    directory = models.ForeignKey(
        Directory,
        on_delete=models.CASCADE,
        related_name="files",
        db_index=True,  # Индексация для ForeignKey
        verbose_name="Родительская директория",
    )
    file = models.FileField(null=True, blank=True, verbose_name="Файл")
    file_path = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Путь к файлу"
    )
    size = models.IntegerField(
        blank=True, null=True, verbose_name="Размер файла"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Дата создания"
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание"
    )
    processing_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="in_queue",
        verbose_name="Статус обработки",
    )
    start_transcription = models.DateTimeField(
        blank=True, null=True, verbose_name="Начало обработки"
    )
    end_transcription = models.DateTimeField(
        blank=True, null=True, verbose_name="Окончание обработки"
    )
    full_time_transcription = models.DateTimeField(
        blank=True, null=True, verbose_name="Общее время обработки"
    )
    original_language = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Язык оригинала"
    )
    original_transcription = models.TextField(
        blank=True, null=True, verbose_name="Текст оригинала"
    )
    russian_transcription = models.TextField(
        blank=True, null=True, verbose_name="Текст перевод на русский язык"
    )

    class Meta:
        indexes = [
            models.Index(
                fields=["directory"]
            ),  # Индекс для фильтрации по директории
            models.Index(
                fields=["created_at"]
            ),  # Индекс для сортировки по дате
        ]
        unique_together = [
            "name",
            "directory",
        ]  # Уникальность имени файла в одной директории

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.file_path:
            self.size = os.path.getsize(self.file_path)
        if self.start_transcription and self.end_transcription:
            self.full_time_transcription = (
                self.end_transcription - self.start_transcription
            )
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    @classmethod
    def add_file(
        cls,
        name: str,
        directory: Directory,
        file_path: Optional[str] = None,
        description: Optional[str] = None,
    ) -> "File":
        """
        Метод для добавления нового файла.
        """
        new_file = cls.objects.create(
            name=name,
            directory=directory,
            file_path=file_path,
            description=description,
        )
        return new_file

    @transaction.atomic
    def delete_file(self) -> None:
        """
        Метод для удаления текущего файла.
        """
        try:
            self.delete()
        except Exception as e:
            logger.error(f"Ошибка при удалении файла {self.name}: {e}")
