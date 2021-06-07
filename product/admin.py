from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from product.models import Category, Product, Images, Comment


class CategoryAdmin(admin.ModelAdmin):  # добавляет в админку фильтр Категории
    list_display = ['title', 'parent', 'status']
    list_filter = ['status', 'parent']


class CategoryAdminTwo(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ['tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count']
    list_display_links = ['indented_title', ]
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


class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id', 'image_tag',)
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'country', 'status', 'image_tag']
    list_filter = ['status', 'category']
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ['status', 'product', 'rate', 'user', 'subject',  'create_at']
    list_filter = ['status']
    readonly_fields = ('product', 'rate', 'comment', 'user', 'subject')
    # inlines = [ProductImageInline]
    # prepopulated_fields = {'slug': ('title',)}


# admin.site.register(Category, CategoryAdmin)  # добавляет в админку Категории
admin.site.register(Category, CategoryAdminTwo)
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)
# admin.site.register(Images)
