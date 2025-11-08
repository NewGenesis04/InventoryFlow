# InventoryFlow API

## Table of Contents
- [Overview](#overview)
- [Features](#-features)
- [Technical Pros](#️-technical-pros)
- [Roles & Permissions](#-roles--permissions)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
- [API Documentation](#api-documentation)
- [Complaints & Feature Requests](#complaints--feature-requests)

## Overview
InventoryFlow is a high-performance, asynchronous inventory management API built with Python using the FastAPI framework. It leverages SQLAlchemy for ORM-based database interactions and Alembic for managing database migrations. It supports **role-based access**, **stock tracking**, **customer/supplier management**, and **automated email notifications** – all wrapped in a sleek, testable REST API.

The system manages inventory by tracking products, stock levels, suppliers, and customers. Incoming and outgoing orders affect the stock accordingly. Admins can monitor stock flow, while customers and suppliers receive relevant email notifications.

Built with scalability, security, and developer experience in mind, InventoryFlow is ideal for small-to-medium businesses, dev demos, or as a base for more complex ERP systems.


## 🌟 Features

- ✅ **CRUD** operations for Products, Categories, Customers, and Suppliers  
- 📦 Track **stock**, incoming & outgoing orders  
- 🔐 **Authentication & Authorization** with JWT and role-based access  
- 📬 **Email notifications** to suppliers and customers  
- 📊 Admin-friendly **dashboard endpoints** with analytics  
- 🔍 **Filtering, and  **searching** for large datasets  
- 🔁 Automated **unit/integration testing** (Pytest)  
- 📄 Interactive **API docs** with Swagger (OpenAPI)  


## ⚙️ Technical Pros
- **FastAPI**: Provides a modern, high-performance web framework for building the API endpoints.
- **SQLAlchemy (Asyncio)**: Implements an asynchronous Object-Relational Mapper (ORM) for efficient and non-blocking database communication.
- **Alembic**: Handles database schema migrations, ensuring database state is consistent with application models.
- **Pydantic**: Enforces strict data validation for request and response models.
- **JWT Authentication**: Secures endpoints using JSON Web Tokens (JWT) for user authentication and authorization.
- **Role-Based Access Control**: Implements user roles (e.g., admin, customer) to restrict access to sensitive operations.
- **Structured Logging**: Utilizes a custom JSON formatter and the Rich library for clear, structured, and easy-to-parse application logs.

## 🔐 Roles & Permissions

| Role     | Capabilities                                                   |
|----------|----------------------------------------------------------------|
| Admin    | Full access to all endpoints and data                          |
| Staff    | Manage inventory, suppliers, customers, and view dashboards    |
| Customer | Limited access: view products, place orders                    |



## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL/MySQL
- SMTP credentials
- UV (optional but recommended)

### Installation

#### Method 1: UV (Recommended)

UV is the recommended way to install and manage InventoryFlow. It's faster and handles dependencies more efficiently.

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/NewGenesis04/InventoryFlow.git
    cd InventoryFlow
    ```

2.  **Install dependencies with UV**:
    ```bash
    uv sync
    ```

#### Method 2: Traditional pip

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/NewGenesis04/InventoryFlow.git
    cd InventoryFlow
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables**:
    -   Copy the example environment file:
        ```bash
        cp .env.example .env
        ```
    -   Edit the `.env` file with your database URL and JWT credentials. See [Environment Variables](#environment-variables).

5.  **Run database migrations**:
    ```bash
    alembic upgrade head
    ```

6.  **Run the application**:
    - With UV (No need to enable virtual environment, UV does that by default with **"uv run"**):
      ```bash
      uv run uvicorn app.main:app --reload
      ```
    - With pip (Ensure virtual environment is enabled first!):  
      ```bash
      uvicorn app.main:app --reload
      ```
    The API will be available at `http://localhost:8000`.

### Environment Variables
Create a `.env` file in the root directory and add the following variables:

| Variable       | Description                  | Example                                               |
| -------------- | ---------------------------- | ----------------------------------------------------- |
| `DB_URL`       | Your database connection URL | `postgresql+asyncpg://user:password@host:port/dbname` |
| `JWT_SECRET_KEY` | Secret key for JWT encoding  | `your-super-secret-key-that-is-long-and-secure`       |
| `JWT_ALGORITHM`  | Algorithm for JWT encoding   | `HS256`                                               |

## API Documentation
### Base URL
`http://localhost:8000`

### Endpoints

#### **Health Check**
---
#### GET /
**Description**: Checks the API status and database connectivity.

**Request**:
No payload required.

**Response**:
```json
{
  "message": "This is the root endpoint of the InventoryFlow API",
  "status": "healthy",
  "database": "connected"
}
```

**Errors**:
- `500 Internal Server Error`: Database connection failed.

#### **Authentication**
---
#### POST /auth/register
**Description**: Registers a new user.

**Request**:
```json
{
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "password": "strongpassword123",
  "role": "admin"
}
```

**Response**:
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john.doe@example.com",
  "role": "admin",
  "created_at": "2023-10-27T10:00:00Z",
  "updated_at": "2023-10-27T10:00:00Z"
}
```

**Errors**:
- `400 Bad Request`: Email already registered.
- `500 Internal Server Error`: Error creating new user.

#### POST /auth/login
**Description**: Authenticates a user and returns JWT tokens.

**Request**:
```json
{
  "email": "john.doe@example.com",
  "password": "strongpassword123"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errors**:
- `400 Bad Request`: Incorrect email or password.

#### GET /auth/me
**Description**: Retrieves the profile of the currently authenticated user. (Requires authentication)

**Request**:
No payload required. Authorization header with bearer token is mandatory.

**Response**:
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john.doe@example.com",
  "role": "admin",
  "created_at": "2023-10-27T10:00:00Z",
  "updated_at": "2023-10-27T10:00:00Z"
}
```

**Errors**:
- `401 Unauthorized`: Invalid token or user not found.

#### **Category Management**
---
#### POST /categories/create
**Description**: Creates a new product category. (Admin role required)

**Request**:
```json
{
  "name": "Electronics",
  "description": "Gadgets and electronic devices"
}
```

**Response**:
```json
{
  "id": 1,
  "name": "Electronics",
  "description": "Gadgets and electronic devices",
  "created_at": "2023-10-27T10:00:00Z",
  "updated_at": "2023-10-27T10:00:00Z"
}
```

**Errors**:
- `401 Unauthorized`: Authentication required.
- `403 Forbidden`: Insufficient permissions.
- `500 Internal Server Error`: Failed to create the category.

#### GET /categories/
**Description**: Retrieves a list of all product categories.

**Request**:
No payload required.

**Response**:
```json
[
  {
    "id": 1,
    "name": "Electronics",
    "description": "Gadgets and electronic devices",
    "created_at": "2023-10-27T10:00:00Z",
    "updated_at": "2023-10-27T10:00:00Z"
  }
]
```

**Errors**:
- `500 Internal Server Error`: Failed to fetch categories.

#### GET /categories/{category_id}
**Description**: Retrieves a single category by its ID.

**Request**:
No payload required.

**Response**:
```json
{
  "id": 1,
  "name": "Electronics",
  "description": "Gadgets and electronic devices",
  "created_at": "2023-10-27T10:00:00Z",
  "updated_at": "2023-10-27T10:00:00Z"
}
```

**Errors**:
- `404 Not Found`: Category not found.
- `500 Internal Server Error`: Failed to fetch the category.

#### PUT /categories/{category_id}
**Description**: Updates an existing category. (Admin role required)

**Request**:
```json
{
  "name": "Consumer Electronics",
  "description": "Updated description for gadgets"
}
```

**Response**:
```json
{
  "id": 1,
  "name": "Consumer Electronics",
  "description": "Updated description for gadgets",
  "created_at": "2023-10-27T10:00:00Z",
  "updated_at": "2023-10-27T10:05:00Z"
}
```

**Errors**:
- `401 Unauthorized`: Authentication required.
- `403 Forbidden`: Insufficient permissions.
- `404 Not Found`: Category not found.
- `500 Internal Server Error`: Failed to update the category.

#### DELETE /categories/{category_id}
**Description**: Deletes a category by its ID. (Admin role required)

**Request**:
No payload required.

**Response**:
`202 Accepted`
```json
{
  "detail": "Category with ID (1) has been deleted successfully"
}
```

**Errors**:
- `401 Unauthorized`: Authentication required.
- `403 Forbidden`: Insufficient permissions.
- `404 Not Found`: Category with the specified ID not found.
- `500 Internal Server Error`: Failed to delete the category.

#### **Product Management**
---
#### POST /products/create
**Description**: Creates a new product. (Admin role required)

**Request**:
```json
{
  "name": "Laptop Pro",
  "description": "A high-end laptop",
  "price": 1200,
  "category_id": 1
}
```

**Response**:
```json
{
  "id": 1,
  "name": "Laptop Pro",
  "description": "A high-end laptop",
  "price": 1200,
  "category_id": 1,
  "created_at": "2023-10-27T10:10:00Z",
  "updated_at": "2023-10-27T10:10:00Z",
  "category": {
    "id": 1,
    "name": "Electronics",
    "description": "Gadgets and electronic devices"
  }
}
```

**Errors**:
- `400 Bad Request`: Product with the same name already exists.
- `401 Unauthorized`: Authentication required.
- `403 Forbidden`: Insufficient permissions.
- `500 Internal Server Error`: Error in creating product.

#### GET /products/
**Description**: Retrieves a list of all products.

**Request**:
No payload required.

**Response**:
```json
[
  {
    "id": 1,
    "name": "Laptop Pro",
    "price": 1200,
    "category_id": 1
  }
]
```

**Errors**:
- `400 Bad Request`: No products found.
- `500 Internal Server Error`: Failed to fetch products.

#### GET /products/{id}
**Description**: Retrieves a single product by its ID.

**Request**:
No payload required.

**Response**:
```json
{
  "id": 1,
  "name": "Laptop Pro",
  "description": "A high-end laptop",
  "price": 1200,
  "category_id": 1,
  "created_at": "2023-10-27T10:10:00Z",
  "updated_at": "2023-10-27T10:10:00Z",
  "category": {
    "id": 1,
    "name": "Electronics",
    "description": "Gadgets and electronic devices"
  }
}
```

**Errors**:
- `400 Bad Request`: No product with the specified ID found.
- `500 Internal Server Error`: Failed to fetch product.

#### PUT /products/{id}
**Description**: Updates an existing product. (Admin role required)

**Request**:
```json
{
  "price": 1150,
  "description": "An updated high-end laptop"
}
```

**Response**:
```json
{
  "id": 1,
  "name": "Laptop Pro",
  "description": "An updated high-end laptop",
  "price": 1150,
  "category_id": 1,
  "created_at": "2023-10-27T10:10:00Z",
  "updated_at": "2023-10-27T10:15:00Z",
  "category": {
    "id": 1,
    "name": "Electronics",
    "description": "Gadgets and electronic devices"
  }
}
```

**Errors**:
- `400 Bad Request`: No product with the specified ID found.
- `401 Unauthorized`: Authentication required.
- `403 Forbidden`: Insufficient permissions.
- `500 Internal Server Error`: Failed to update product.

#### DELETE /products/{id}
**Description**: Deletes a product by its ID. (Admin role required)

**Request**:
No payload required.

**Response**:
`202 Accepted`
```json
{
  "detail": "Product with ID (1) has been deleted successfully"
}
```

**Errors**:
- `400 Bad Request`: No product with the specified ID found.
- `401 Unauthorized`: Authentication required.
- `403 Forbidden`: Insufficient permissions.
- `500 Internal Server Error`: Failed to delete product.

#### **Stock Management**
---
#### GET /stocks/
**Description**: Retrieves a list of all stock entries.

**Request**:
No payload required.

**Response**:
```json
[
  {
    "id": 1,
    "product_id": 1,
    "available_quantity": 50,
    "batch_number": "BATCH001"
  }
]
```

**Errors**:
- `404 Not Found`: No stock entries found.
- `500 Internal Server Error`: Failed to fetch stock entries.

#### GET /stocks/{id}
**Description**: Retrieves a specific stock entry by its ID.

**Request**:
No payload required.

**Response**:
```json
{
  "id": 1,
  "product_id": 1,
  "available_quantity": 50,
  "batch_number": "BATCH001",
  "expiry_date": "2025-12-31T00:00:00Z",
  "created_at": "2023-10-27T10:20:00Z",
  "updated_at": "2023-10-27T10:20:00Z",
  "product": {
    "id": 1,
    "name": "Laptop Pro",
    "price": 1200
  }
}
```

**Errors**:
- `404 Not Found`: Stock with the specified ID not found.
- `500 Internal Server Error`: Failed to fetch stock entry.

#### PATCH /stocks/{id}
**Description**: Manually updates the quantity of a stock entry. (Admin role required)

**Request**:
```json
{
  "available_quantity": 45
}
```

**Response**:
```json
{
  "id": 1,
  "product_id": 1,
  "available_quantity": 45,
  "batch_number": "BATCH001",
  "expiry_date": "2025-12-31T00:00:00Z",
  "created_at": "2023-10-27T10:20:00Z",
  "updated_at": "2023-10-27T10:25:00Z",
  "product": {
    "id": 1,
    "name": "Laptop Pro",
    "price": 1200
  }
}
```

**Errors**:
- `401 Unauthorized`: Authentication required.
- `403 Forbidden`: Insufficient permissions.
- `404 Not Found`: Stock with the specified ID not found.
- `500 Internal Server Error`: Failed to update stock entry.

#### **Incoming Order Management**
---
#### POST /incoming/
**Description**: Creates a new incoming order from a supplier and updates stock. (Admin role required)

**Request**:
```json
{
  "supplier_id": 1,
  "product_id": 1,
  "batch_number": "BATCH001",
  "quantity": 50,
  "unit_cost": 800,
  "supply_date": "2023-10-27T10:20:00Z",
  "expiry_date": "2025-12-31T00:00:00Z"
}
```

**Response**:
```json
{
  "id": 1,
  "supplier_id": 1,
  "product_id": 1,
  "batch_number": "BATCH001",
  "quantity": 50,
  "unit_cost": 800,
  "total_cost": 40000,
  "supply_date": "2023-10-27T10:20:00Z",
  "status": "pending",
  "supplier": { "id": 1, "name": "Supplier A" },
  "product": { "id": 1, "name": "Laptop Pro" }
}
```

**Errors**:
- `401 Unauthorized`: Authentication required.
- `403 Forbidden`: Insufficient permissions.
- `404 Not Found`: Product or Supplier not found.
- `500 Internal Server Error`: Failed to create incoming order.

#### GET /incoming/
**Description**: Retrieves a list of all incoming orders.

**Request**:
No payload required.

**Response**:
```json
[
  {
    "id": 1,
    "supplier_id": 1,
    "product_id": 1,
    "quantity": 50,
    "total_cost": 40000,
    "status": "pending"
  }
]
```

**Errors**:
- `404 Not Found`: No incoming orders found.
- `500 Internal Server Error`: Failed to fetch incoming orders.

#### GET /incoming/{id}
**Description**: Retrieves a specific incoming order by its ID.

**Request**:
No payload required.

**Response**:
```json
{
  "id": 1,
  "supplier_id": 1,
  "product_id": 1,
  "batch_number": "BATCH001",
  "quantity": 50,
  "unit_cost": 800,
  "total_cost": 40000,
  "supply_date": "2023-10-27T10:20:00Z",
  "status": "pending",
  "supplier": { "id": 1, "name": "Supplier A" },
  "product": { "id": 1, "name": "Laptop Pro" }
}
```

**Errors**:
- `404 Not Found`: Incoming order with the specified ID not found.
- `500 Internal Server Error`: Failed to fetch incoming order.

#### **Outgoing Order Management**
---
#### POST /outgoing/
**Description**: Creates a new outgoing order for a customer and decreases stock. (Admin role required)

**Request**:
```json
{
  "customer_id": 1,
  "product_id": 1,
  "stock_id": 1,
  "quantity": 2,
  "order_date": "2023-10-27T11:00:00Z"
}
```

**Response**:
```json
{
  "id": 1,
  "customer_id": 1,
  "product_id": 1,
  "stock_id": 1,
  "quantity": 2,
  "unit_price": 1200,
  "total_price": 2400,
  "order_date": "2023-10-27T11:00:00Z",
  "status": "pending",
  "customer": { "id": 1, "first_name": "Jane", "last_name": "Smith" },
  "product": { "id": 1, "name": "Laptop Pro" }
}
```

**Errors**:
- `400 Bad Request`: Insufficient stock.
- `401 Unauthorized`: Authentication required.
- `403 Forbidden`: Insufficient permissions.
- `404 Not Found`: Stock, Product, or Customer not found.
- `500 Internal Server Error`: Failed to create outgoing order.

#### GET /outgoing/
**Description**: Retrieves a list of all outgoing orders.

**Request**:
No payload required.

**Response**:
```json
[
  {
    "id": 1,
    "customer_id": 1,
    "product_id": 1,
    "quantity": 2,
    "total_price": 2400,
    "status": "pending"
  }
]
```

**Errors**:
- `404 Not Found`: No outgoing orders found.
- `500 Internal Server Error`: Failed to fetch outgoing orders.

#### GET /outgoing/{id}
**Description**: Retrieves a specific outgoing order by its ID.

**Request**:
No payload required.

**Response**:
```json
{
  "id": 1,
  "customer_id": 1,
  "product_id": 1,
  "stock_id": 1,
  "quantity": 2,
  "unit_price": 1200,
  "total_price": 2400,
  "order_date": "2023-10-27T11:00:00Z",
  "status": "pending",
  "customer": { "id": 1, "first_name": "Jane", "last_name": "Smith" },
  "product": { "id": 1, "name": "Laptop Pro" }
}
```

**Errors**:
- `404 Not Found`: Outgoing order with the specified ID not found.
- `500 Internal Server Error`: Failed to fetch outgoing order.

## Complaints & Feature Requests

We welcome feedback, feature requests, and bug reports! To submit a complaint or request a new feature, please open a GitHub issue:

1. Navigate to the [Issues](https://github.com/NewGenesis04/InventoryFlow/issues) page
2. Click on **New Issue**
3. Use the appropriate tag:
   - 🐛 **`bug`** - For reporting bugs or problems
   - ✨ **`feature`** - For suggesting new features or improvements
   - 📝 **`documentation`** - For documentation-related issues
   - ❓ **`question`** - For general questions

Please provide as much detail as possible to help us understand and address your request effectively.
