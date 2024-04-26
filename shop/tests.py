from django.test import TestCase
from.models import Category, Product


class CategoryModelTests(TestCase):
    def test_category_model(self):
        category = Category(name='Test Category')
        self.assertEqual(str(category), 'Test Category')


class ProductModelTests(TestCase):
    def test_product_model(self):
        category = Category.objects.create(name='Test Category')
        product = Product(name='Test Product', category=category)
        self.assertEqual(str(product), 'Test Product')
