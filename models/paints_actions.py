from typing import List, Optional, Generator
from .paint import Paint
from .collection import Collection


def find_paint_by_id(paints: List[Paint], paint_id: int) -> Optional[Paint]:
    """Найти картину по ее ID."""
    for paint in paints:
        if paint.id == paint_id:
            return paint
    return None


def is_paint_exists(paints: List[Paint], paint_id: int) -> bool:
    """Проверить существование картины по ID."""
    return find_paint_by_id(paints, paint_id) is not None


def create_paint(
    paints: List[Paint],
    collections: List[Collection],
    paint_id: int,
    title: str,
    artist: str,
    size: str,
    year: int,
    image: str,
    technic: str,
    material: str,
    collection_id: int,
) -> str:
    """Создать новую картину и добавить ее в коллекцию."""
    if is_paint_exists(paints, paint_id):
        return "=== Картина уже существует ==="

    collection = None
    for col in collections:
        if col.id == collection_id:
            collection = col
            break

    if not collection:
        # Если коллекция не найдена, создадим дефолтную или вернем ошибку
        collection = Collection(
            collection_id,
            "Основная коллекция",
            "Автоматически созданная коллекция",
        )
        collections.append(collection)

    new_paint = Paint(
        paint_id=paint_id,
        title=title,
        artist=artist,
        size=size,
        year=year,
        image=image,
        technic=technic,
        material=material,
        collection=collection,
    )
    paints.append(new_paint)
    return "=== Картина создана ==="


def delete_paint(paints: List[Paint], paint_id: int) -> str:
    """Удалить картину по ID."""
    paint = find_paint_by_id(paints, paint_id)
    if paint:
        paints.remove(paint)
        return "=== Картина удалена ==="
    return "=== Картины не существует ==="


def find_paints(paints: List[Paint], query: str) -> List[Paint]:
    """Найти картины по подстроке в названии или авторе."""
    query_lower = query.lower()
    return [
        p for p in paints
        if query_lower in p.title.lower() or query_lower in p.artist.lower()
    ]


def filter_paints_by_year(
    paints: List[Paint], min_year: int, max_year: int
) -> Generator[Paint, None, None]:
    """Генератор отбора картин по диапазону годов создания."""
    for paint in paints:
        if paint.is_created_in_period(min_year, max_year):
            yield paint


def sort_paints_by_year(
    paints: List[Paint], reverse: bool = False
) -> List[Paint]:
    """Отсортировать картины по году с использованием lambda-функции."""
    return sorted(paints, key=lambda p: p.year, reverse=reverse)


def get_paints_in_collection(
    paints: List[Paint], collection_id: int
) -> List[Paint]:
    """Получить список всех картин в заданной коллекции."""
    return [p for p in paints if p.collection.id == collection_id]


def get_paint_status(is_found: bool) -> str:
    """Вернуть текстовый статус (преемственность с ПР1/ПР2)."""
    if is_found:
        return "=== Картина найдена ==="
    return "=== Картины не существует ==="


def show_paints(paints: List[Paint]) -> str:
    """Вывести список всех картин."""
    if not paints:
        print("=== Список картин пуст ===")
        return "=== Конец списка ==="

    for paint in paints:
        print(paint)
        print("=============")
    return "=== Конец списка ==="
