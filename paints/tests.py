from django.test import Client, TestCase, override_settings

from db.import_json import main as import_json_data


class GalleryPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        import_json_data()

    def setUp(self):
        self.client = Client()

    def test_homepage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Система учёта работ художника"
        )

    def test_paints_list_page_uses_sqlite_data(self):
        response = self.client.get("/paints/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Демон сидящий")
        self.assertContains(response, "Царевна-Лебедь")

    def test_paint_detail_page(self):
        response = self.client.get("/paints/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Михаил Александрович Врубель"
        )
        self.assertContains(response, "Масло")
        self.assertContains(
            response, "Шедевры Государственной"
        )

    def test_unknown_paint_returns_404(self):
        response = self.client.get("/paints/999/")
        self.assertEqual(response.status_code, 404)
        self.assertContains(
            response, "Работа не найдена", status_code=404
        )

    def test_paint_search(self):
        response = self.client.get(
            "/paints/search/", {"min_year": "1890", "max_year": "1895"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Демон сидящий")
        self.assertNotContains(response, "Царевна-Лебедь")

    def test_paint_search_rejects_invalid_range(self):
        response = self.client.get(
            "/paints/search/", {"min_year": "1900", "max_year": "1890"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "корректный диапазон годов"
        )

    def test_collections_list_page(self):
        response = self.client.get("/collections/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Шедевры Государственной"
        )
        self.assertContains(response, "Работ: 2")

    def test_collection_detail_page(self):
        response = self.client.get("/collections/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Демон сидящий")
        self.assertContains(response, "Царевна-Лебедь")

    def test_unknown_collection_returns_404(self):
        response = self.client.get("/collections/999/")
        self.assertEqual(response.status_code, 404)

    def test_statistics_page(self):
        response = self.client.get("/collections/statistics/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Всего произведений в каталоге: 2"
        )
        self.assertContains(
            response, "Михаил Александрович Врубель"
        )

    @override_settings(DEBUG=False)
    def test_unknown_url_uses_custom_404(self):
        response = self.client.get("/not-a-real-page/")
        self.assertEqual(response.status_code, 404)
        self.assertContains(
            response,
            "404 — страница не найдена",
            status_code=404,
        )
