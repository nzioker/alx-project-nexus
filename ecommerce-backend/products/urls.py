from django.urls import path
from .views import (
    CategoryListCreateView,
    CategoryDetailView,
    ProductListView,
    ProductCreateView,
    ProductDetailView,
    ProductReviewListCreateView,
    ProductReviewDetailView,
    ProductStatisticsView
)

urlpatterns = [
    # Category endpoints
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    
    # Product endpoints
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    
    # Review endpoints
    path('products/<slug:slug>/reviews/', 
         ProductReviewListCreateView.as_view(), 
         name='product-reviews'),
    path('reviews/<int:pk>/', 
         ProductReviewDetailView.as_view(), 
         name='review-detail'),
    
    # Statistics
    path('statistics/', ProductStatisticsView.as_view(), name='product-statistics'),
]