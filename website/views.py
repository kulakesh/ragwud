from django.shortcuts import render
from super.models import Category

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def gallery(request):
    return render(request, 'gallery.html')

def contact(request):
    return render(request, 'contact.html')

def products(request):
    categories = Category.objects.prefetch_related('products').order_by('id').all()
    return render(request, 'products.html', {
        'categories': categories
    })