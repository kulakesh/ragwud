from django.shortcuts import render
from accounts.decorators import admin_required
from .forms import ProductCreateForm, ProductUpdateForm, CategoryForm
from django.contrib import messages
from django.shortcuts import redirect
from .models import Product, Category

@admin_required
def admin_dashboard(request):
    return render(request, "admin/dashboard.html")

@admin_required
def products(request, product_id=None):
    products = Product.objects.all()
    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('admin_products')
    elif request.method == 'GET':
        product = Product.objects.filter(id=product_id).first()
        if product:
            form = ProductCreateForm(instance=product)
        else:
            form = ProductCreateForm()

    return render(request, "admin/product.html", {"form": form, "products": products, "product_id": product_id})

@admin_required
def product_edit(request, product_id):
    products = Product.objects.all()
    product = Product.objects.filter(id=product_id).first()
    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('admin_products')
    else:
        form = ProductUpdateForm(instance=product)

    return render(request, "admin/product.html", {"form": form, "product": product, "products": products, "product_id": product_id})

def product_delete(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if product:
        product.delete()
        messages.success(request, 'Product deleted successfully!')
    else:
        messages.error(request, 'Product not found.')
    return redirect('admin_products')

@admin_required
def category(request, category_id=None):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = CategoryForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('admin_category')
    elif request.method == 'GET':
        category = Category.objects.filter(id=category_id).first()
        if category:
            form = CategoryForm(instance=category)
        else:
            form = CategoryForm()

    return render(request, "admin/category.html", {"form": form, "categories": categories, "category_id": category_id})

@admin_required
def category_edit(request, category_id):
    category = Category.objects.filter(id=category_id).first()
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('admin_category')
    else:
        form = CategoryForm(instance=category)

    return render(request, "admin/category.html", {"form": form, "category": category})

@admin_required
def category_delete(request, category_id):
    category = Category.objects.filter(id=category_id).first()
    if category:
        category.delete()
        messages.success(request, 'Category deleted successfully!')
    else:
        messages.error(request, 'Category not found.')
    return redirect('admin_category')