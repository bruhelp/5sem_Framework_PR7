from django.test import TestCase


class CollectionPagesTests(TestCase):
    def test_collections_list_page(self):
        response = self.client.get("/collections/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Шедевры Государственной")

    def test_collection_detail_page(self):
        response = self.client.get("/collections/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Демон сидящий")

    def test_unknown_collection_returns_404(self):
        response = self.client.get("/collections/999/")
        self.assertEqual(response.status_code, 404)
