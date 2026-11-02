# Система учёта работ художника

Учебное приложение для учёта произведений искусства и галерейных коллекций.
Консольная версия сохранена, веб-интерфейс реализован на Django.

## Возможности

- просмотр каталога картин и карточек отдельных работ;
- просмотр галерейных коллекций и входящих в них произведений;
- отображение автора, года, размера, техники, материала и изображения;
- получение каталога и коллекций из SQLite через SQL-запросы;
- поиск произведений по диапазону лет создания;
- статистика по коллекциям и художникам;
- перенос исходных данных из JSON в SQLite с помощью отдельного скрипта;
- общая навигация и единое оформление страниц.

## Технологии

- Python 3.11 или новее;
- Django 5.2;
- Django Template Language;
- HTML5, CSS3, JavaScript;
- Bootstrap 5.3;
- JSON;
- pytest;
- flake8.

## Слой базы данных после ПР7

Для хранения предметных данных используется SQLite (`data/art_gallery.sqlite`),
а не Django ORM. Исходные JSON-файлы сохранены как источник и для обратной
совместимости предыдущих практических работ.

Таблицы:

- `collections`: `id INTEGER PRIMARY KEY`, `name TEXT NOT NULL`,
  `description TEXT NOT NULL`;
- `paints`: `id INTEGER PRIMARY KEY`, `title TEXT`, `artist TEXT`,
  `size TEXT`, `year INTEGER`, `image TEXT`, `technic TEXT`,
  `material TEXT`, `collection_id INTEGER`.

`paints.collection_id` — внешний ключ на `collections.id`. Схема хранится в
`sql/schema.sql`; подключение и включение внешних ключей реализовано в
`db/database.py`; `db/import_json.py` переносит данные из JSON с помощью
`executemany()`, параметров `?` и транзакции. Проверенные запросы, включая
SELECT, WHERE, JOIN, COUNT, GROUP BY и HAVING, находятся в `sql/queries.sql`.

Django-представления получают результаты через `sqlite3.Row` и передают их
шаблонам через context. Из SQLite формируются каталог, карточка произведения,
список и состав коллекций, поиск по диапазону лет и статистика.

## Архитектура веб-интерфейса после ПР6

HTML вынесен из Python-представлений в Django-шаблоны. Общая структура
страниц находится в `templates/base.html`. Дочерние шаблоны используют
`extends` и `block`, повторяющиеся элементы подключаются через `include`.
Данные передаются из view-функций через контекст; шаблоны используют
циклы, условия и фильтры. Ссылки строятся именованными URL с пространствами
имён приложений. CSS, изображение и JavaScript подключаются через `static`.

Основные URL:

| URL | Назначение |
| --- | --- |
| `/` | Главная |
| `/paints/` | Каталог произведений |
| `/paints/<paint_id>/` | Карточка произведения |
| `/collections/` | Список коллекций |
| `/collections/<collection_id>/` | Состав коллекции |
| `/paints/search/` | Поиск работ по диапазону лет |
| `/collections/statistics/` | Статистика по коллекциям и художникам |

## Данные и предметная область

Предметные классы `Paint` и `Collection`, JSON-файлы и консольный интерфейс
из предыдущих практических работ сохранены. Веб-страницы каталога и коллекций
теперь читают актуальные данные из SQLite. Django ORM и формы Django пока не
используются.

## Структура проекта

- `gallery/` — настройки и корневая маршрутизация Django;
- `homepage/` — главная страница;
- `paints/` — каталог и карточка произведения, шаблоны приложения;
- `collections_app/` — список и состав коллекций, шаблоны приложения;
- `templates/` — базовый шаблон, навигация и страница 404;
- `static/` — собственные CSS, JavaScript и логотип;
- `models/` — предметные классы и операции;
- `data/` — исходные JSON-файлы и база `art_gallery.sqlite`;
- `db/` — подключение к SQLite и импорт JSON;
- `sql/` — схема и набор SQL-запросов;
- `storage.py` — загрузка и сохранение JSON для предыдущих этапов;
- `tests/` — тесты предметной области.

## Запуск через venv

### Windows PowerShell

```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python -m db.import_json
python manage.py check
python manage.py runserver
```

### Windows CMD

```bat
py -3.11 -m venv venv
venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python -m db.import_json
python manage.py check
python manage.py runserver
```

### macOS / Linux

```bash
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python -m db.import_json
python manage.py check
python manage.py runserver
```

Откройте http://127.0.0.1:8000/. Для выхода из окружения выполните
`deactivate`.

## Проверки

В активированном виртуальном окружении:

```bash
python manage.py check
pytest -v
python manage.py test
flake8 . --extend-exclude=venv
```

## Консольная версия

```bash
python main.py
```

## Дальнейшее развитие

На следующих практических работах слой прямого доступа через sqlite3 может
быть заменён Django ORM; JSON и консольная реализация предыдущих этапов при
этом остаются в проекте как история развития.
