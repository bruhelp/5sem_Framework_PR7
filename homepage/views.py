from django.shortcuts import render


def index(request):
    """Показать главную страницу проекта."""
    return render(request, "homepage/index.html")


def page_not_found(request, exception):
    """Вернуть пользовательскую страницу с HTTP-статусом 404."""
    return render(
        request,
        "404.html",
        status=404,
    )
