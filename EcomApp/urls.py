from django.urls import path
from .views import home, single_product, category_product, about_us, contact_us

urlpatterns = [
    path('', home, name='home-page'),

    path('about-us/', about_us, name='about-us-page'),
    path('contact/', contact_us, name='contact-page'),

    path('product/<int:id>/<slug:slug>/',
         single_product, name='product-details'),
    path('category/<slug:slug>/', category_product, name='category-products')
]
