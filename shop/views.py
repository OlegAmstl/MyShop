from django.shortcuts import render, get_object_or_404

from .models import Category, Product


def product_list(request, category_slug=None):
    """
    List all products, or all products in a particular category.
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/products/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    """
    Display a single product.
    """
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request,
                  'shop/products/detail.html',
                  {'product': product})
