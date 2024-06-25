import os

# Токен ботика
BOT_TOKEN = '6789115472:AAGKYbONCUFmgl99xGwVVbG8CPrD_4iO_ok'

# Данные для подключения к базе данных
DB_CONFIG = {
    "dbname": os.getenv("waterdbbot"),
    "user": os.getenv("postgres"),
    "password": os.getenv("postgres"),
    "host": os.getenv("localhost"),
    "port": os.getenv("5432"),
}
