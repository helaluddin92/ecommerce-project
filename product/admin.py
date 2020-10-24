from django.contrib import admin
from .models import Category, Product, ProductImage
from mptt.admin import DraggableMPTTAdmin

# Register your models here.


class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_cumulative_count',
            cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                                                Product,
                                                'category',
                                                'products_count',
                                                cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'


admin.site.register(Category, CategoryAdmin)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 5


# admin.site.register(ProductImage)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'status',
                    'image_category', 'updated_at', 'image_tag', ]
    readonly_fields = ('image_tag',)
    list_filter = ['title', 'created_at']
    list_per_page = 10
    search_fields = ['title', 'new_price', 'detail']
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Product, ProductAdmin)
