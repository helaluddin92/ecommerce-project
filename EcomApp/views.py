from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from .models import *
from product.models import *
from .forms import SearchForm
# Create your views here.


def home(request):
    settings = Setting.objects.get(id=1)
    slider_products = Product.objects.filter(
        image_category='Slider').order_by('-id')
    banner_products = Product.objects.filter(
        image_category='Banner').order_by('-id')
    banner_2_products = Product.objects.filter(
        image_category='Banner').order_by('id')[:3]
    featured_products = Product.objects.filter(image_category='Featured')
    new_products = Product.objects.filter(
        image_category='Product').order_by('-id')
    categories = Category.objects.all()

    context = {
        'settings': settings,
        'slider_products': slider_products,
        'banner_products': banner_products,
        'banner_2_products': banner_2_products,
        'featured_products': featured_products,
        'new_products': new_products,
        'categories': categories
    }
    return render(request, "home.html", context=context)


def about_us(request):
    settings = Setting.objects.get(id=1)
    categories = Category.objects.all()
    context = {
        'settings': settings,
        'categories': categories
    }
    return render(request, 'about-us.html', context=context)


def contact_us(request):
    settings = Setting.objects.get(id=1)
    categories = Category.objects.all()
    form = ContactMessageForm
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, 'You message has been sent')
            return HttpResponseRedirect(reverse('contact-page'))
    context = {
        'settings': settings,
        'categories': categories,
        'form': form
    }
    return render(request, 'contact.html', context=context)


def search(request):
    query = request.GET['q']
    sel_category = request.GET.get('cat_id', None)
    if query:
        category_products = Category.objects.all()
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(detail__icontains=query),
            image_category__in=('Product', 'Featured')
        )
        count = products.count()
    elif sel_category:
        category_products = get_object_or_404(Category, pk=sel_category)
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(detail__icontains=query),
            image_category__in=('Product', 'Featured'),
            category=category_products,
        )
        count = products.count()
        if category_products:
            products = products.filter(
                category__title__icontains=category_products.title,
                image_category__in=('Product', 'Featured')
            )
            count = products.count()
    else:
        query = ""
        products = None
    categories = Category.objects.all()
    settings = Setting.objects.get(id=1)
    context = {
        'query': query,
        'products': products,
        'category_products': category_products,
        'categories': categories,
        'count': count,
        'settings': settings
    }
    return render(request, 'category_product.html', context)


def single_product(request, id, slug):
    settings = Setting.objects.get(id=1)
    single_product = Product.objects.get(id=id)
    single_product_images = ProductImage.objects.filter(product__id=id)
    single_product_categories = Product.objects.filter(
        category=single_product.category, image_category='Product')
    categories = Category.objects.all()
    context = {
        'settings': settings,
        'single_product': single_product,
        'single_product_images': single_product_images,
        'single_product_categories': single_product_categories,
        'categories': categories
    }
    return render(request, 'single-product.html', context=context)


def category_product(request, slug):
    settings = Setting.objects.get(id=1)
    categories = Category.objects.all()
    category_products = Category.objects.get(slug=slug)
    products = Product.objects.filter(
        category=category_products, image_category__in=('Product', 'Featured'))[:12]
    count = products.count()
    context = {
        'settings': settings,
        'categories': categories,
        'category_products': category_products,
        'products': products,
        'count': count
    }

    return render(request, 'category_product.html', context=context)
