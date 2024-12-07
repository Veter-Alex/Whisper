import os

from django.db import transaction
from loguru import logger


@transaction.atomic
def sync_database_with_directory(root_path=None, parent_directory=None):
    """
    Синхронизирует базу данных с файловой системой, начиная с заданной директории.

    :param root_path: Абсолютный путь к корневой директории на файловой системе.
    :param parent_directory: Объект Directory, представляющий родительскую директорию в базе данных.
    """
    from .models import Directory, File
    from config.models import AppSetting
    
    if not root_path:
        root_path = AppSetting.objects.get(key="root_directory").value
    
    # Получаем список всех поддиректорий и файлов, которые уже есть в базе данных
    # для текущей директории.
    # Для директорий используем `parent_directory` для фильтрации по родителю.
    logger.info(f"Синхронизация {root_path}")
    existing_directories = {
        directory.name: directory
        for directory in Directory.objects.filter(parent=parent_directory)
    }
    # Для файлов используем `parent_directory` для фильтрации по директории, в которой они находятся.
    existing_files = {
        file.name: file for file in File.objects.filter(directory=parent_directory)
    }

    # Получаем список всех элементов (файлов и директорий) на файловой системе
    # для текущей директории (root_path).
    try:
        file_system_entries = os.listdir(root_path)
    except FileNotFoundError:
        # Если директория не существует, выводим сообщение и выходим из функции.
        logger.error(f"Директория {root_path} не найдена.")
        return

    # === Обработка директорий ===
    for entry in file_system_entries:
        full_path = os.path.abspath(
            os.path.join(root_path, entry)
        )  # Получаем абсолютный путь.

        if os.path.isdir(full_path):  # Если элемент — это директория.
            if entry not in existing_directories:
                # Если директория не существует в базе данных:
                # Добавляем новую директорию, используя метод `add_directory` из модели Directory.
                new_directory = Directory.add_directory(
                    name=entry, parent=parent_directory
                )
                logger.info(f"Добавлена новая директория: {entry}")
            else:
                # Если директория уже есть в базе данных:
                # Извлекаем её из словаря `existing_directories` для последующей обработки.
                new_directory = existing_directories.pop(entry)

            # Рекурсивно вызываем функцию для обработки содержимого поддиректории.
            sync_database_with_directory(full_path, new_directory)

    # === Обработка файлов ===
    for entry in file_system_entries:
        full_path = os.path.abspath(
            os.path.join(root_path, entry)
        )  # Получаем абсолютный путь.

        if os.path.isfile(full_path):  # Если элемент — это файл.
            if entry not in existing_files:
                # Если файл не существует в базе данных:
                # Добавляем новый файл, используя метод `add_file` из модели File.
                File.add_file(name=entry, directory=parent_directory)
                logger.info(f"Добавлен новый файл: {entry}")
            else:
                # Если файл уже есть в базе данных:
                # Удаляем его из словаря `existing_files`, так как он больше не требует обработки.
                existing_files.pop(entry)

    # === Удаление отсутствующих директорий ===
    for directory_name, directory_obj in existing_directories.items():
        # Все оставшиеся директории в `existing_directories` отсутствуют на файловой системе.
        # Удаляем их из базы данных, используя метод `delete_directory` из модели Directory.
        directory_obj.delete_directory()
        logger.info(f"Удалена директория: {directory_name}")

    # === Удаление отсутствующих файлов ===
    for file_name, file_obj in existing_files.items():
        # Все оставшиеся файлы в `existing_files` отсутствуют на файловой системе.
        # Удаляем их из базы данных, используя метод `delete_file` из модели File.
        file_obj.delete_file()
        logger.info(f"Удален файл: {file_name}")
