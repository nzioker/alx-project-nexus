#  E-Commerce Backend API

A robust, scalable Django REST Framework backend for modern e-commerce applications. This project simulates a real-world development environment with emphasis on scalability, security, and performance.

![Django](https://img.shields.io/badge/Django-4.2.7-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![DRF](https://img.shields.io/badge/DRF-3.14.0-red)
![JWT](https://img.shields.io/badge/JWT-Authentication-orange)

##  Features

###  Authentication & Authorization
- **JWT-based authentication** with access & refresh tokens
- **Custom User model** with email as username
- **Role-based permissions** (Admin, Vendor, Customer)
- **Secure password validation** and hashing

###  Product Management
- **Full CRUD operations** for products and categories
- **Product variants** (sizes, colors, etc.)
- **Image management** with multiple product images
- **Inventory tracking** with stock alerts
- **Pricing management** with discounts and comparisons

###  Advanced API Features
- **Filtering** by category, price range, vendor, stock status
- **Sorting** by price, date, name, rating
- **Pagination** with configurable page sizes
- **Full-text search** across product names and descriptions
- **Hierarchical categories** with parent-child relationships

###  Performance & Optimization
- **Database indexing** for optimized queries
- **Select/Prefetch related** to prevent N+1 queries
- **PostgreSQL** for production-grade performance
- **Query optimization** for large datasets

###  API Documentation
- **Auto-generated Swagger/OpenAPI** documentation
- **Interactive Swagger UI** at `/swagger/`
- **ReDoc documentation** at `/redoc/`
- **Complete API schema** in JSON/YAML formats

##  Prerequisites

- Python 3.9+
- PostgreSQL 12+ (or Docker)
- pip (Python package manager)
- Git


