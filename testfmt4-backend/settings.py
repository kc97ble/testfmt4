import os

from dotenv import load_dotenv

load_dotenv(verbose=True)

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER") or "/tmp"
DATABASE_FILE = os.getenv("DATABASE_FILE") or "/tmp/testfmt4.sqlite3"
