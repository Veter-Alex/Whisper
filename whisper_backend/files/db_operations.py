from loguru import logger
import psycopg2
from psycopg2 import sql


def create_database():
    from django.core.management import call_command
    from django.contrib.auth.models import User

    logger.info(f"Проверка базы данных.")

    """Создание базы данных, если она не существует."""
    # Параметры подключения к PostgreSQL
    # TODO Настроить получение настроек для подключения к БД из файла настроек
    db_name = "veteran_db"  # База данных приложения
    db_user = "postgres"  # Имя пользователя для подключения к postgres
    db_password = "root"  # Пароль для подключения к postgres
    db_host = "localhost"  # Хост postgres
    db_port = "5432"  # Порт postgres

    try:
        # Соединение с PostgreSQL
        conn = psycopg2.connect(
            # dbname="postgres",
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
            # Создаем базу данных
            logger.info(f"База '{db_name}' отсутствует.")
            logger.info(f"Создание базы данных '{db_name}'.")
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
            )
            logger.info(f"База данных '{db_name}' успешно создана.")
        cursor.close()
        conn.close()
    except Exception as err:
        logger.error(f"Ошибка при создании базы данных: {err}")
    else:
        try:
            # Применяем миграции
            logger.info("Применение миграций...")
            call_command("makemigrations")
            call_command("migrate")
            logger.info("Миграции успешно применены.")
        except Exception as err:
            logger.error(f"Ошибка при создании миграций: {err}")

        try:
            # Создание супер пользователя Django
            logger.info("Создание супер пользователя Django...")

            # Настройка Django окружения
            # Не нужно настраивать!! Вызывает ошибку!!
            # Вызывается в manage.py, один раз!!
            # os.environ.setdefault(
            #     "DJANGO_SETTINGS_MODULE",
            #     "whisper_backend.settings",
            # )
            # django.setup()

            # Данные супер пользователя
            # TODO Загружать данные из файла
            username = "root"
            email = "admin@mail.com"
            password = "root"

            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username, email=email, password=password
                )
                logger.info("Супер пользователь Django успешно создан.")
            else:
                logger.info(
                    f"Супер пользователь Django '{username}' уже существует."
                )
        except Exception as err:
            logger.error(f"Ошибка при создании супер пользователя: {err}")
