import os
import subprocess
import sys

from loguru import logger


def create_database():
    import psycopg2
    from psycopg2 import sql

    """Создание базы данных, если она не существует."""
    # Параметры подключения к PostgreSQL
    db_name = "veteran_db"
    db_user = "postgres"
    db_password = "root"
    db_host = "localhost"
    db_port = "5432"

    try:
        # Соединение с PostgreSQL
        conn = psycopg2.connect(
            dbname="postgres",
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Проверяем, существует ли база данных
        cursor.execute(
            f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}';"
        )
        exists = cursor.fetchone()

        if exists:
            logger.info(f"База данных '{db_name}' уже существует.")
        else:
            # Выводим путь к Python
            print("Путь Python ", sys.executable)
            # Создаем базу данных
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
            )
            logger.info(f"База данных '{db_name}' успешно создана.")

            # Применяем миграции
            logger.info("Применение миграций...")
            run_subprocess_with_virtualenv(
                "D:\\Programming\\Projects\\Python\\Whisper\\whisper_backend\\.venv\\Scripts\\activate.bat",
                "python manage.py migrate",
            )
            logger.info("Миграции успешно выполнены.")

        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Ошибка при создании базы данных: {e}")


def run_subprocess_with_virtualenv(activate_script, command):
    """Запуск команды с активированным виртуальным окружением."""
    try:
        # Путь к бат-файлу для активации виртуального окружения
        command_to_run = f"call {activate_script} && {command}"

        # Запуск команды с активацией виртуального окружения
        result = subprocess.run(
            command_to_run, shell=True, check=True, capture_output=True, text=True
        )
        logger.info(f"Команда выполнена успешно: {command}")
        logger.info(f"Вывод: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Ошибка при выполнении команды {command}: {e}")
        logger.error(f"Стандартный вывод: {e.stdout}")
        logger.error(f"Стандартная ошибка: {e.stderr}")
