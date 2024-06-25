#type: ignore
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Данные для подключения к базе данных
DB_CONFIG = {
    "dbname": os.getenv("YOUR_DATABASE_NAME"),
    "user": os.getenv("YOUR_USERNAME"),
    "password": os.getenv("YOUR_PASSWORD"),
    "host": os.getenv("YOUR_HOST"),
    "port": os.getenv("YOUR_PORT"),
}
