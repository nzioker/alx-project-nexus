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
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    
    path('products/<slug:slug>/reviews/', 
         ProductReviewListCreateView.as_view(), 
         name='product-reviews'),
    path('reviews/<int:pk>/', 
         ProductReviewDetailView.as_view(), 
         name='review-detail'),
    
    path('statistics/', ProductStatisticsView.as_view(), name='product-statistics'),
]