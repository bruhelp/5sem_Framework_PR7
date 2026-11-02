from .collection import Collection


class Paint:
    """Произведение искусства (картина)."""

    def __init__(
        self,
        paint_id: int,
        title: str,
        artist: str,
        size: str,
        year: int,
        image: str,
        technic: str,
        material: str,
        collection: Collection,
    ) -> None:
        self.id = paint_id
        self.title = title
        self.artist = artist
        self.size = size
        self.year = year
        self.image = image
        self.technic = technic
        self.material = material
        self.collection = collection

    def is_created_in_period(self, min_year: int, max_year: int) -> bool:
        """Проверить, создана ли картина в заданном диапазоне годов."""
        return min_year <= self.year <= max_year

    @staticmethod
    def validate_year(year: int) -> bool:
        """Проверить корректность года создания."""
        return year > 0

    def __str__(self) -> str:
        return (
            f"ID: {self.id} | Работы: '{self.title}' ({self.year}) — "
            f"Художник: {self.artist}, Техника: {self.technic}, "
            f"Материал: {self.material}, Коллекция: {self.collection.name}"
        )
