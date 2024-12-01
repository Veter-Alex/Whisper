import os

from django.apps import AppConfig, apps
from django.core.exceptions import ObjectDoesNotExist


class FilesConfig(AppConfig):
    # default_auto_field = "django.db.models.BigAutoField"
    name = "files"

    def ready(self):
        self.check_and_sync_directory()

    def check_and_sync_directory(self):
        root_directory = self.get_root_directory()

        if not root_directory:
            print(
                "Корневая директория не найдена в настройках. Пожалуйста, создайте настройку 'root_directory'."
            )
            return

        self.sync_directory_and_files(root_directory)

    def get_root_directory(self):
        # Пытаемся получить настройку "root_directory", если не существует — создаём с дефолтным значением
        Setting = apps.get_model("config.Setting")
        try:
            setting = Setting.objects.get(key="root_directory")
            return setting.value
        except ObjectDoesNotExist:
            # Создаём настройку с дефолтным значением
            Setting.objects.create(key="root_directory", value="Null")
            return "Null"

    def sync_directory_and_files(self, root_path):
        if not os.path.exists(root_path):
            print(f"Ошибка: Корневая директория '{root_path}' не существует.")
            return

        self.traverse_directory(root_path)

    def traverse_directory(self, path, parent_directory=None):
        for entry in os.scandir(path):
            if entry.is_dir():
                # Создание или обновление каталога Directory
                Directory = apps.get_model("files.Directory")
                directory, created = Directory.objects.get_or_create(
                    name=entry.name,  # Используем имя каталога
                    parent=parent_directory,  # Родительский каталог
                )
                if created:
                    print(f"Создан каталог: {directory.name}")
                self.traverse_directory(entry.path, parent_directory=directory)
            elif entry.is_file():
                # Создание или обновление файла File
                File = apps.get_model("files.File")
                file_size = os.path.getsize(entry.path)  # Размер файла в байтах
                file, created = File.objects.get_or_create(
                    name=entry.name, defaults={"size": file_size}
                )
                if created:
                    print(f"Создан файл: {file.name} размер {file.size} байт")
                # Устанавливаем директорию для файла
                file.directory = parent_directory
                file.save()
