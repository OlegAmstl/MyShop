from django.test import TestCase
from.models import Category


class TestCategory(TestCase):

    def test_category_model(self):
        """
        Test the Category model.
        """
        category = Category(name='Test Category', slug='test-category')
        assert category.name == 'Test Category'
        assert category.slug == 'test-category'
        assert str(category) == 'Test Category'