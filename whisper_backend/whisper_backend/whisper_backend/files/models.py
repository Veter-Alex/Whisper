import os

from django.db import models


# Модель для хранения директорий
class Directory(models.Model):
    name = models.CharField(max_length=255)  # Имя директории
    parent = models.ForeignKey(
        "self",  # Ссылка на саму себя для построения иерархии
        on_delete=models.CASCADE,  # При удалении родителя удаляются и все его дочерние директории
        null=True,  # Корневые директории могут не иметь родителя
        blank=True,  # Корневые директории могут быть пустыми
        related_name="subdirectories",  # Имя для доступа к дочерним директориям через родителя
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания директории

    def __str__(self):
        # При выводе объекта в строковом формате будем показывать родителя, если он есть
        return f"{self.name} (Parent: {self.parent.name if self.parent else 'None'})"

    @classmethod
    def add_directory(cls, name, parent=None):
        """
        Метод для добавления новой директории.
        """
        directory = cls.objects.create(name=name, parent=parent)
        return directory

    def delete_directory(self):
        """
        Метод для удаления текущей директории, включая все дочерние директории и файлы.
        Удаление дочерних объектов происходит автоматически благодаря CASCADE.
        """
        # Удалим саму директорию
        self.delete()


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
        verbose_name="Родительская директория",
    )
    file = models.FileField(upload_to="files/")
    size = models.IntegerField(blank=True, null=True, verbose_name="Размер файла")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
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

    def save(self, *args, **kwargs):
        if self.file:
            self.size = os.path.getsize(self.file.path)
        if self.start_transcription and self.end_transcription:
            # Рассчитываем разницу во времени
            self.full_time_transcription = (
                self.end_transcription - self.start_transcription
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @classmethod
    def add_file(cls, name, directory, file, description=None):
        """
        Метод для добавления нового файла.
        """
        new_file = cls.objects.create(
            name=name, directory=directory, file=file, description=description
        )
        return new_file

    def delete_file(self):
        """
        Метод для удаления текущего файла.
        """
        # Удалим файл с диска
        if self.file:
            os.remove(self.file.path)
        # Удалим запись в базе данных
        self.delete()
