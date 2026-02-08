from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, NumberFilter, CharFilter, BooleanFilter
from django.db.models import Q, Avg, Count
from django.shortcuts import get_object_or_404
from .models import Category, Product, ProductReview
from .serializers import (
    CategorySerializer, ProductSerializer, ProductListSerializer,
    ProductReviewSerializer
)
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class ProductFilter(FilterSet):
    min_price = NumberFilter(field_name="price", lookup_expr='gte')
    max_price = NumberFilter(field_name="price", lookup_expr='lte')
    category = CharFilter(field_name="category__slug")
    # REMOVED: vendor = CharFilter(field_name="vendor__email")
    in_stock = BooleanFilter(field_name="quantity", lookup_expr='gt')
    featured = BooleanFilter(field_name="is_featured")

    class Meta:
        model = Product
        # REMOVED 'vendor' from fields list
        fields = ['category', 'min_price', 'max_price', 'in_stock', 'featured']

class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = ProductFilter
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']
    search_fields = ['name', 'description', 'sku', 'category__name']

    def get_queryset(self):
        # REMOVED: .select_related('category', 'vendor')
        queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')

        # Additional filtering logic
        category_slug = self.request.query_params.get('category')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug, is_active=True)
            # Get all child categories
            child_categories = category.children.filter(is_active=True)
            category_ids = [category.id] + list(child_categories.values_list('id', flat=True))
            queryset = queryset.filter(category_id__in=category_ids)

        # Filter by search query
        search_query = self.request.query_params.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains(search_query)) |
                Q(sku__icontains(search_query)) |
                Q(category__name__icontains(search_query))
            )

        return queryset

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    # REMOVED: perform_create method (no vendor to set)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    lookup_field = 'slug'

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class ProductReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product_slug = self.kwargs['slug']
        return ProductReview.objects.filter(
            product__slug=product_slug,
            is_approved=True
        ).select_related('user')

    def perform_create(self, serializer):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        serializer.save(user=self.request.user, product=product)

class ProductReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(is_approved=False)

# COMPLETELY REMOVED or REPLACED: ProductStatisticsView
# This view was entirely vendor-specific and should be removed
# If you want general stats, create a new view for admins only
class ProductStatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Only allow staff/admin users to see statistics
        if not request.user.is_staff:
            return Response(
                {'detail': 'You do not have permission to view statistics.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # General statistics for all products
        total_products = Product.objects.count()
        active_products = Product.objects.filter(is_active=True).count()
        out_of_stock = Product.objects.filter(quantity=0).count()
        low_stock = Product.objects.filter(
            quantity__gt=0,
            quantity__lte=models.F('low_stock_threshold')
        ).count()

        avg_rating_result = ProductReview.objects.filter(
            is_approved=True
        ).aggregate(avg_rating=Avg('rating'))

        avg_rating = avg_rating_result['avg_rating'] or 0

        return Response({
            'total_products': total_products,
            'active_products': active_products,
            'out_of_stock': out_of_stock,
            'low_stock': low_stock,
            'average_rating': round(avg_rating, 2),
        })