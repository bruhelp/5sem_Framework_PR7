from typing import Dict, Any


class Collection:
    """Коллекция произведений искусства в галерее."""

    def __init__(
        self,
        collection_id: int,
        name: str,
        description: str,
    ) -> None:
        self.id = collection_id
        self.name = name
        self.description = description

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> "Collection":
        """Создать объект коллекции из набора данных."""
        return cls(
            collection_id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
        )

    def __str__(self) -> str:
        return f"Коллекция #{self.id}: {self.name} — {self.description}"
