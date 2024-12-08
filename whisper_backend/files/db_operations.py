import os

import psycopg2
from django.contrib.auth.models import User
from django.core.management import call_command
from dotenv import load_dotenv
from loguru import logger
from psycopg2 import sql

# Загрузка переменных окружения
load_dotenv()


def check_or_create_database() -> None:
    """Проверяет наличие базы данных, при необходимости создаёт её."""
    db_name = os.getenv("DB_NAME", "veteran_db")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "root")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")

    try:
        # Подключение к PostgreSQL
        conn = psycopg2.connect(
            user=db_user, password=db_password, host=db_host, port=db_port
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Проверяем наличие базы данных
        cursor.execute(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s;",
            (db_name,),
        )
        exists = cursor.fetchone()

        if exists:
            logger.info(f"База данных '{db_name}' уже существует.")
        else:
            logger.info(f"База данных '{db_name}' отсутствует. Создаём...")
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
            )
            logger.info(f"База данных '{db_name}' успешно создана.")

        cursor.close()
        conn.close()
    except Exception as err:
        logger.error(f"Ошибка при проверке/создании базы данных: {err}")
        raise


def apply_migrations() -> None:
    """Применяет миграции Django."""
    try:
        logger.info("Применение миграций...")
        call_command("makemigrations")
        call_command("migrate")
        logger.info("Миграции успешно применены.")
    except Exception as err:
        logger.error(f"Ошибка при применении миграций: {err}")
        raise


def create_superuser() -> None:
    """Создаёт суперпользователя Django."""
    try:
        username = os.getenv("SUPERUSER_NAME", "root")
        email = os.getenv("SUPERUSER_EMAIL", "admin@mail.com")
        password = os.getenv("SUPERUSER_PASSWORD", "root")

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username, email=email, password=password
            )
            logger.info(f"Суперпользователь '{username}' успешно создан.")
        else:
            logger.info(f"Суперпользователь '{username}' уже существует.")
    except Exception as err:
        logger.error(f"Ошибка при создании суперпользователя: {err}")
        raise


def main_db_operations() -> None:
    """Основной процесс."""
    try:
        logger.info("Инициализация базы данных...")
        check_or_create_database()
        apply_migrations()
        create_superuser()
        logger.info("Инициализация завершена успешно.")
    except Exception as err:
        logger.error(f"Произошла ошибка: {err}")


if __name__ == "__main__":
    main_db_operations()
