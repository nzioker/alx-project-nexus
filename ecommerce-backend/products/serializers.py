from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductVariant, ProductReview

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'parent', 
                  'is_active', 'children', 'product_count')
        read_only_fields = ('slug', 'children', 'product_count')
    
    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializer(obj.children.filter(is_active=True), many=True).data
        return []
    
    def get_product_count(self, obj):
        return obj.products.filter(is_active=True).count()

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'alt_text', 'is_primary', 'order')

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ('id', 'name', 'value', 'sku', 'price_adjustment', 'quantity')

class ProductReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = ProductReview
        fields = ('id', 'user_email', 'user_name', 'rating', 'title', 
                  'comment', 'is_approved', 'created_at', 'updated_at')
        read_only_fields = ('is_approved', 'created_at', 'updated_at')

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.filter(is_active=True),
        source='category',
        write_only=True
    )
    
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'description', 'price', 'compare_at_price',
            'cost_per_item', 'sku', 'barcode', 'quantity', 'low_stock_threshold',
            'category', 'category_id', 'is_active', 'is_featured',
            'in_stock', 'low_stock', 'discount_percentage', 'images', 'variants',
            'reviews', 'average_rating', 'review_count', 'created_at', 'updated_at'
        )
        read_only_fields = ('slug', 'created_at', 'updated_at')
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.filter(is_approved=True)
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 2)
        return 0
    
    def get_review_count(self, obj):
        return obj.reviews.filter(is_approved=True).count()
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value
    
    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative")
        return value

class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'price', 'compare_at_price',
            'discount_percentage', 'category_name', 'image_url',
            'in_stock', 'is_featured', 'created_at'
        )
    
    def get_image_url(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return primary_image.image.url
        first_image = obj.images.first()
        if first_image:
            return first_image.image.url
        return None