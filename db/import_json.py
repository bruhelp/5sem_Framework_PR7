"""Перенос исходных JSON-данных в SQLite."""
import json

from db.database import BASE_DIR, get_connection

DATA_DIR = BASE_DIR / "data"


def load_json(filename):
    """Загрузить JSON-файл в Python."""
    with (DATA_DIR / filename).open(encoding="utf-8") as file:
        return json.load(file)


def import_data(connection):
    """Заменить содержимое таблиц данными из исходных JSON-файлов.

    Данные добавляются пакетно с помощью executemany().
    """
    collections = load_json("collections.json")
    paints = load_json("paints.json")

    connection.execute("DELETE FROM paints")
    connection.execute("DELETE FROM collections")
    connection.executemany(
        """
        INSERT INTO collections (id, name, description)
        VALUES (?, ?, ?)
        """,
        [
            (item["id"], item["name"], item.get("description", ""))
            for item in collections
        ],
    )
    connection.executemany(
        """
        INSERT INTO paints (
            id, title, artist, size, year, image, technic, material,
            collection_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                item["id"], item["title"], item["artist"],
                item.get("size", ""), item["year"],
                item.get("image", ""), item.get("technic", ""),
                item.get("material", ""), item["collection_id"],
            )
            for item in paints
        ],
    )


def main():
    """Создать схему и импортировать данные в одной транзакции.

    При ошибке изменения отменяются.
    """
    schema_path = BASE_DIR / "sql" / "schema.sql"
    schema = schema_path.read_text(encoding="utf-8")
    connection = get_connection()
    try:
        connection.executescript(schema)
        import_data(connection)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    main()
