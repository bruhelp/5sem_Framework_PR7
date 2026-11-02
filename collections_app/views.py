"""Представления галерейных коллекций на основе SQLite."""
from contextlib import closing

from django.shortcuts import render

from db.database import get_connection


def collections_list(request):
    """Показать коллекции и количество работ в каждой из них."""
    with closing(get_connection()) as connection:
        collections = connection.execute(
            """
            SELECT collections.id, collections.name, collections.description,
                   COUNT(paints.id) AS paints_count
            FROM collections
            LEFT JOIN paints ON collections.id = paints.collection_id
            GROUP BY collections.id, collections.name, collections.description
            ORDER BY collections.name
            """
        ).fetchall()
    return render(request, "collections/collection_list.html", {
        "collections": collections,
    })


def collection_detail(request, collection_id):
    """Показать коллекцию и связанные произведения."""
    with closing(get_connection()) as connection:
        collection = connection.execute(
            "SELECT * FROM collections WHERE id = ?",
            (collection_id,),
        ).fetchone()
        paints = []
        if collection is not None:
            paints = connection.execute(
                """
                SELECT id, title, artist, year
                FROM paints
                WHERE collection_id = ?
                ORDER BY year, title
                """,
                (collection_id,),
            ).fetchall()
    return render(
        request,
        "collections/collection_detail.html",
        {"collection": collection, "paints": paints},
        status=404 if collection is None else 200,
    )


def statistics(request):
    """Показать сводные показатели по коллекциям и художникам."""
    with closing(get_connection()) as connection:
        collection_stats = connection.execute(
            """
            SELECT collections.name AS collection_name,
                   COUNT(paints.id) AS paints_count
            FROM collections
            LEFT JOIN paints ON collections.id = paints.collection_id
            GROUP BY collections.id, collections.name
            ORDER BY paints_count DESC, collections.name
            """
        ).fetchall()
        artist_stats = connection.execute(
            """
            SELECT artist, COUNT(*) AS paints_count,
                   MIN(year) AS first_year, MAX(year) AS last_year
            FROM paints
            GROUP BY artist
            ORDER BY paints_count DESC, artist
            """
        ).fetchall()
        total = connection.execute(
            "SELECT COUNT(*) AS paints_count FROM paints"
        ).fetchone()["paints_count"]
    return render(
        request,
        "collections/statistics.html",
        {
            "collection_stats": collection_stats,
            "artist_stats": artist_stats,
            "total_paints": total,
        },
    )
