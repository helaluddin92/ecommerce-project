from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import *
from product.models import *
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
    context = {
        'settings': settings,
        'categories': categories,
        'category_products': category_products,
        'products': products
    }

    return render(request, 'category_product.html', context=context)
