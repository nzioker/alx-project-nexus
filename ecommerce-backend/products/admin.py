from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVariant, ProductReview

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'is_active', 'product_count')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)} 

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Number of Products'

admin.site.register(Category, CategoryAdmin)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1 # Number of empty forms to show
    fields = ('image', 'alt_text', 'is_primary', 'order')

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('name', 'value', 'sku', 'price_adjustment', 'quantity')

class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    extra = 0
    can_delete = False
    readonly_fields = ('user', 'rating', 'title', 'comment', 'created_at')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'price', 'quantity', 'is_active', 'is_featured', 'created_at')
    list_filter = ('is_active', 'is_featured', 'category')
    search_fields = ('name', 'description', 'sku')
    list_editable = ('price', 'quantity', 'is_active', 'is_featured')
    prepopulated_fields = {'slug': ('name',)} 

    inlines = [ProductImageInline, ProductVariantInline, ProductReviewInline]

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'category')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'compare_at_price', 'cost_per_item', 'sku', 'barcode', 'quantity', 'low_stock_threshold')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
    )

admin.site.register(Product, ProductAdmin)

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'title', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('product__name', 'user__email', 'title', 'comment')
    list_editable = ('is_approved',) # Quickly approve reviews from the list
    actions = ['approve_reviews', 'disapprove_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = "Approve selected reviews"

    def disapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_reviews.short_description = "Disapprove selected reviews"

admin.site.register(ProductReview, ProductReviewAdmin)