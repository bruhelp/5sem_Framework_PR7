def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число с обработкой ошибок."""
    while True:
        try:
            val_str = input(prompt).strip()
            return int(val_str)
        except ValueError:
            print("Ошибка: введите корректное целое число!")


def input_non_empty(prompt: str) -> str:
    """Запросить непустую строку."""
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("Ошибка: поле не может быть пустым!")
