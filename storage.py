import json
import os
from typing import List

from models import Collection, Paint


def load_collections(filename: str) -> List[Collection]:
    """Загрузить список коллекций из JSON-файла."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        return [Collection.from_data(item) for item in data]
    except (json.JSONDecodeError, OSError) as error:
        print(f"Ошибка при чтении файла {filename}: {error}")
        return []


def save_collections(
    filename: str,
    collections: List[Collection],
) -> None:
    """Сохранить список коллекций в JSON-файл."""
    try:
        directory = os.path.dirname(filename)
        if directory:
            os.makedirs(directory, exist_ok=True)
        data = [
            {
                "id": collection.id,
                "name": collection.name,
                "description": collection.description,
            }
            for collection in collections
        ]
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except OSError as error:
        print(f"Ошибка при записи файла {filename}: {error}")


def load_paints(
    filename: str,
    collections: List[Collection],
) -> List[Paint]:
    """Загрузить картины и восстановить связи с коллекциями."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        paints = []
        for item in data:
            collection_id = item.get("collection_id", 1)
            collection = next(
                (
                    current for current in collections
                    if current.id == collection_id
                ),
                None,
            )
            if collection is None:
                collection = Collection(
                    collection_id,
                    "Коллекция по умолчанию",
                    "",
                )
                collections.append(collection)
            paints.append(
                Paint(
                    paint_id=item["id"],
                    title=item["title"],
                    artist=item["artist"],
                    size=item["size"],
                    year=item["year"],
                    image=item["image"],
                    technic=item["technic"],
                    material=item["material"],
                    collection=collection,
                )
            )
        return paints
    except (json.JSONDecodeError, OSError, KeyError, TypeError) as error:
        print(f"Ошибка при чтении файла {filename}: {error}")
        return []


def save_paints(filename: str, paints: List[Paint]) -> None:
    """Сохранить список картин в JSON-файл."""
    try:
        directory = os.path.dirname(filename)
        if directory:
            os.makedirs(directory, exist_ok=True)
        data = [
            {
                "id": paint.id,
                "title": paint.title,
                "artist": paint.artist,
                "size": paint.size,
                "year": paint.year,
                "image": paint.image,
                "technic": paint.technic,
                "material": paint.material,
                "collection_id": paint.collection.id,
            }
            for paint in paints
        ]
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except OSError as error:
        print(f"Ошибка при записи файла {filename}: {error}")
