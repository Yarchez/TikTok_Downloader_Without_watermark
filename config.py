from dotenv import load_dotenv, find_dotenv

import os

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPIDAPI_TOKEN = os.getenv("RAPIDAPI_TOKEN")

