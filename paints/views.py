"""Django-представления каталога на основе SQLite."""
from contextlib import closing

from django.shortcuts import render

from db.database import get_connection


def paints_list(request):
    """Показать каталог работ, полученный SQL-запросом из SQLite."""
    with closing(get_connection()) as connection:
        paints = connection.execute(
            """
            SELECT paints.id, paints.title, paints.artist, paints.year,
                   paints.image, collections.name AS collection_name
            FROM paints
            JOIN collections ON paints.collection_id = collections.id
            ORDER BY paints.year, paints.title
            """
        ).fetchall()
    return render(
        request,
        "paints/paint_list.html",
        {
            "paints": paints,
            "page_title": "Каталог произведений",
        },
    )


def paint_detail(request, paint_id):
    """Показать произведение и связанную с ним коллекцию."""
    with closing(get_connection()) as connection:
        paint = connection.execute(
            """
            SELECT paints.*, collections.name AS collection_name,
                   collections.description AS collection_description
            FROM paints
            JOIN collections ON paints.collection_id = collections.id
            WHERE paints.id = ?
            """,
            (paint_id,),
        ).fetchone()
    return render(
        request,
        "paints/paint_detail.html",
        {"paint": paint},
        status=404 if paint is None else 200,
    )


def paint_search(request):
    """Найти картины, созданные в указанном диапазоне лет."""
    min_year = request.GET.get("min_year", "")
    max_year = request.GET.get("max_year", "")
    paints = []
    search_error = ""
    if min_year or max_year:
        try:
            first_year = int(min_year)
            last_year = int(max_year)
            if first_year < 1 or last_year < first_year:
                raise ValueError
        except (TypeError, ValueError):
            search_error = (
                "Укажите корректный диапазон годов."
            )
        else:
            with closing(get_connection()) as connection:
                paints = connection.execute(
                    """
                    SELECT id, title, artist, year
                    FROM paints
                    WHERE year BETWEEN ? AND ?
                    ORDER BY year, title
                    """,
                    (first_year, last_year),
                ).fetchall()
    return render(
        request,
        "paints/paint_search.html",
        {
            "paints": paints,
            "min_year": min_year,
            "max_year": max_year,
            "search_error": search_error,
            "searched": bool(min_year or max_year) and not search_error,
        },
    )
