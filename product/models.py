from django.db import models
from django.utils.html import mark_safe
# Django mptt
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.


class Category(MPTTModel):
    status = (
        ('True', 'True'),
        ('False', 'False')
    )

    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    title = models.CharField(max_length=200)
    keywords = models.CharField(max_length=100)
    image = models.ImageField(
        blank=True, upload_to='Category/', default='category.png')
    status = models.CharField(max_length=20, choices=status)
    slug = models.SlugField(null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title


class Product(models.Model):
    status = (
        ('True', 'True'),
        ('False', 'False')
    )

    IMAGE_CATEGORY = (
        ('Slider', 'Slider'),
        ('Featured', 'Featured'),
        ('Banner', 'Banner'),
        ('Product', 'Product')
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    keywords = models.CharField(max_length=100)
    image = models.ImageField(
        blank=True, upload_to='Product/', default='product.png')
    image_category = models.CharField(
        choices=IMAGE_CATEGORY, default='Product', max_length=20)
    new_price = models.DecimalField(decimal_places=2, max_digits=15, default=0)
    sell_offer = models.CharField(
        max_length=100, blank=True, null=True, default='10% off')
    old_price = models.DecimalField(decimal_places=2, max_digits=15)
    amount = models.IntegerField(default=0)
    min_amount = models.IntegerField(default=3)
    detail = models.TextField()
    status = models.CharField(max_length=20, choices=status)
    slug = models.SlugField(null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" width="60" height="60"'.format(self.image.url))
    image_tag.short_description = 'Image'

    def discount_price(self):
        if self.new_price < self.old_price:
            return f'{(((self.old_price - self.new_price)*100)/self.old_price): .0f}'
        else:
            return ''


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(blank=True, upload_to='Product/')

    def __str__(self):
        if self.title:
            return self.title
        else:
            return 'self.product.title'
