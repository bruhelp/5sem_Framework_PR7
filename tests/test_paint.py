from models import Paint, Collection
from models.paints_actions import (
    create_paint,
    delete_paint,
    find_paints,
    sort_paints_by_year,
    filter_paints_by_year,
    get_paint_status,
)


def test_paint_creation():
    col = Collection(1, "Тест", "Описание")
    paint = Paint(
        1, "Демон", "Врубель", "100х200", 1890,
        "http://", "Масло", "Холст", col
    )
    assert paint.id == 1
    assert paint.title == "Демон"
    assert paint.collection is col


def test_paint_is_created_in_period():
    col = Collection(1, "Тест", "Описание")
    paint = Paint(
        1, "Демон", "Врубель", "100х200", 1890,
        "http://", "Масло", "Холст", col
    )
    assert paint.is_created_in_period(1880, 1900)
    assert not paint.is_created_in_period(1900, 1920)


def test_create_paint_action():
    paints = []
    collections = []
    res = create_paint(
        paints, collections, 1, "Демон", "Врубель",
        "100х200", 1890, "http://", "Масло", "Холст", 1
    )
    assert len(paints) == 1
    assert paints[0].title == "Демон"
    assert res == "=== Картина создана ==="


def test_delete_paint_action():
    paints = []
    collections = []
    create_paint(
        paints, collections, 1, "Демон", "Врубель",
        "100х200", 1890, "http://", "Масло", "Холст", 1
    )
    res = delete_paint(paints, 1)
    assert len(paints) == 0
    assert res == "=== Картина удалена ==="


def test_find_paints():
    paints = []
    collections = []
    create_paint(
        paints, collections, 1, "Демон сидящий", "Врубель",
        "100х200", 1890, "http://", "Масло", "Холст", 1
    )
    results = find_paints(paints, "демон")
    assert len(results) == 1
    assert results[0].id == 1


def test_sort_paints_by_year():
    col = Collection(1, "Тест", "")
    paints = [
        Paint(1, "П2", "А", "1х1", 1900, "http", "М", "Х", col),
        Paint(2, "П1", "А", "1х1", 1890, "http", "М", "Х", col),
    ]
    sorted_p = sort_paints_by_year(paints)
    assert sorted_p[0].year == 1890
    assert sorted_p[1].year == 1900


def test_filter_paints_by_year():
    col = Collection(1, "Тест", "")
    paints = [
        Paint(1, "П1", "А", "1х1", 1890, "http", "М", "Х", col),
        Paint(2, "П2", "А", "1х1", 1900, "http", "М", "Х", col),
    ]
    filtered = list(filter_paints_by_year(paints, 1880, 1895))
    assert len(filtered) == 1
    assert filtered[0].id == 1


def test_get_paint_status():
    assert get_paint_status(True) == "=== Картина найдена ==="
    assert get_paint_status(False) == "=== Картины не существует ==="
