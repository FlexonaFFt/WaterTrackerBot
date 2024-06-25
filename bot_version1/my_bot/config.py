import os

# Данные для подключения к базе данных
DB_CONFIG = {
    "dbname": os.getenv("waterdbbot"),
    "user": os.getenv("postgres"),
    "password": os.getenv("postgres"),
    "host": os.getenv("localhost"),
    "port": os.getenv("5432"),
}
