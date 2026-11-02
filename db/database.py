"""Подключение к SQLite для веб-приложения и скриптов.

Модуль также содержит общий путь к файлу базы данных.
"""
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "art_gallery.sqlite"


def get_connection():
    """Открыть соединение с включёнными внешними ключами.

    Для результатов используется фабрика строк с доступом по имени поля.
    """
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection
