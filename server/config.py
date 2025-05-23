import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

SMTP_URL = str(os.getenv('SMTP_SSL')) + str(os.getenv('SMTP_PORT'))
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
SECRET_KEY = os.getenv('SECRET_KEY')
DB_URL = os.getenv('DATABASE')
GEOCODE = os.getenv('GEOCODE')