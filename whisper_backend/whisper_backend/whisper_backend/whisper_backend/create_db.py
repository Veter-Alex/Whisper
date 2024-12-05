import psycopg2
from psycopg2 import sql


def create_database():
    # Параметры подключения к PostgreSQL
    db_name = "veteran_db"
    db_user = "postgres"
    db_password = "root"
    db_host = "localhost"
    db_port = "5432"

    # Соединение с PostgreSQL
    conn = psycopg2.connect(
        dbname="postgres",
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
    )

    conn.autocommit = True  # Для выполнения CREATE DATABASE

    cursor = conn.cursor()

    # Проверяем, существует ли база данных
    cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}';")
    exists = cursor.fetchone()

    if exists:
        print(f"База данных '{db_name}' уже существует.")
    else:
        # Если базы данных нет, создаём её
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
        print(f"База данных '{db_name}' успешно создана.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    create_database()
