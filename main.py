from typing import List

from models import Collection, Paint
from models.paints_actions import (
    create_paint,
    delete_paint,
    filter_paints_by_year,
    find_paint_by_id,
    find_paints,
    get_paint_status,
    get_paints_in_collection,
    show_paints,
    sort_paints_by_year,
)
from storage import (
    load_collections,
    load_paints,
    save_collections,
    save_paints,
)
from utils import input_int, input_non_empty

COLLECTIONS_FILE = "data/collections.json"
PAINTS_FILE = "data/paints.json"


def main() -> None:
    """Точка запуска приложения и обработка главного меню."""
    collections: List[Collection] = load_collections(COLLECTIONS_FILE)
    paints: List[Paint] = load_paints(PAINTS_FILE, collections)

    while True:
        print("\n=== Система учёта работ художника (ООП) ===")
        print(
            "Введите команду: Список, Удалить, Создать, Посмотреть, "
            "Найти, Фильтр, Сортировка, Коллекция, Закончить"
        )
        command = input("Команда: ").strip()

        if command == "Список":
            show_paints(paints)
        elif command == "Удалить":
            paint_id = input_int("Введите id работы: ")
            result = delete_paint(paints, paint_id)
            save_paints(PAINTS_FILE, paints)
            print(result)
        elif command == "Создать":
            paint_id = input_int("Введите id работы: ")
            title = input_non_empty("Введите название работы: ")
            artist = input_non_empty("Введите автора работы: ")
            size = input_non_empty("Введите размер работы: ")
            year = input_int("Введите год работы: ")
            image = input_non_empty("Введите ссылку на изображение: ")
            technic = input_non_empty(
                "Введите технику выполнения работы: "
            )
            material = input_non_empty("Введите материал работы: ")
            collection_id = input_int(
                "Введите id коллекции, к которой работа принадлежит: "
            )
            result = create_paint(
                paints,
                collections,
                paint_id,
                title,
                artist,
                size,
                year,
                image,
                technic,
                material,
                collection_id,
            )
            save_paints(PAINTS_FILE, paints)
            save_collections(COLLECTIONS_FILE, collections)
            print(result)
        elif command == "Посмотреть":
            paint_id = input_int("Введите id работы: ")
            paint = find_paint_by_id(paints, paint_id)
            print(get_paint_status(paint is not None))
            if paint is not None:
                print(paint)
        elif command == "Найти":
            query = input_non_empty("Введите подстроку для поиска: ")
            results = find_paints(paints, query)
            print(f"Найдено работ: {len(results)}")
            show_paints(results)
        elif command == "Фильтр":
            min_year = input_int("Введите начальный год: ")
            max_year = input_int("Введите конечный год: ")
            filtered = list(
                filter_paints_by_year(paints, min_year, max_year)
            )
            print(f"Работы за период {min_year}-{max_year}:")
            show_paints(filtered)
        elif command == "Сортировка":
            sorted_paints = sort_paints_by_year(paints)
            print("=== Картины, отсортированные по году ===")
            show_paints(sorted_paints)
        elif command == "Коллекция":
            collection_id = input_int("Введите id коллекции: ")
            collection_paints = get_paints_in_collection(
                paints, collection_id
            )
            print(f"=== Работы из коллекции {collection_id} ===")
            show_paints(collection_paints)
        elif command == "Закончить":
            print("До свидания!")
            break
        else:
            print("Неизвестная команда. Попробуйте снова.")


if __name__ == "__main__":
    main()
