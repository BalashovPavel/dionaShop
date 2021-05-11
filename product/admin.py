
from django.contrib import admin

from product.models import Category, Product, Images


class CategoryAdmin(admin.ModelAdmin):  # добавляет в админку фильтр Категории
    list_display = ['title', 'parent', 'status']
    list_filter = ['status', 'parent']


class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'image_tag']
    list_filter = ['status', 'category']
    inlines = [ProductImageInline]


admin.site.register(Category, CategoryAdmin)  # добавляет в админку Категории
admin.site.register(Product, ProductAdmin)
admin.site.register(Images)