from models import Collection
from models.paints_actions import get_paints_in_collection
from models import Paint


def test_collection_creation():
    col = Collection.from_data(
        {"id": 1, "name": "Тест", "description": "Описание"}
    )
    assert col.id == 1
    assert col.name == "Тест"
    assert "Тест" in str(col)


def test_get_paints_in_collection():
    col = Collection(1, "Тест", "")
    paints = [
        Paint(1, "П1", "А", "1х1", 1890, "http", "М", "Х", col),
        Paint(2, "П2", "А", "1х1", 1900, "http", "М", "Х", col),
    ]
    col_paints = get_paints_in_collection(paints, 1)
    assert len(col_paints) == 2
