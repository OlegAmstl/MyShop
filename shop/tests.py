from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from .models import Category, Product
from .views import product_list, product_detail


class CategoryModelTests(TestCase):
    """
    Tests category.
    """

    def test_category_model(self):
        category = Category(name='Test Category')
        self.assertEqual(str(category), 'Test Category')


class ProductModelTests(TestCase):
    """
    Tests product.
    """
    def test_product_model(self):
        category = Category.objects.create(name='Test Category')
        product = Product(name='Test Product', category=category)
        self.assertEqual(str(product), 'Test Product')


class ProductListViewTest(TestCase):
    """
    Tests product list view.
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.category1 = Category.objects.create(name='Category 1')
        self.category2 = Category.objects.create(name='Category 2')
        self.product1 = Product.objects.create(name='Product 1',
                                               category=self.category1,
                                               price=100)
        self.product2 = Product.objects.create(name='Product 2',
                                               category=self.category2,
                                               price=200)

    def test_product_list_view_with_no_category(self):
        request = self.factory.get('/')
        response = product_list(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('categories', response.context)
        self.assertIn('products', response.context)
        self.assertEqual(len(response.context['categories']), 2)
        self.assertEqual(len(response.context['products']), 2)
        self.assertIn(self.category1, response.context['categories'])
        self.assertIn(self.category2, response.context['categories'])
        self.assertIn(self.product1, response.context['products'])
        self.assertIn(self.product2, response.context['products'])

    def test_product_list_view_with_category(self):
        request = self.factory.get('/category/category-1/')
        response = product_list(request, 'category-1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('categories', response.context)
        self.assertIn('products', response.context)
        self.assertEqual(len(response.context['categories']), 1)
        self.assertEqual(len(response.context['products']), 1)
        self.assertIn(self.category1, response.context['categories'])
        self.assertNotIn(self.category2, response.context['categories'])
        self.assertIn(self.product1, response.context['products'])
        self.assertNotIn(self.product2, response.context['products'])


class ProductDetailViewTests(TestCase):
    """
    Tests product detail view.
    """

    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            price=10.00,
            description='This is a test product.',
            category=self.category,
            available=True
        )
        self.url = reverse('shop:product-detail',
                           args=[self.product.id, self.product.slug])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/products/detail.html')
        self.assertContains(response, self.product.name)
        self.assertContains(response, self.product.price)
        self.assertContains(response, self.product.description)

    def test_get_for_unavailable_product(self):
        self.product.available = False
        self.product.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)
