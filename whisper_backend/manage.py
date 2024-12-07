#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Точка входа в приложение."""
    # Создаем базу данных только для команд runserver и migrate
    if "runserver" in sys.argv or "migrate" in sys.argv:
        from whisper_backend.create_db import create_database

        create_database()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "whisper_backend.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
