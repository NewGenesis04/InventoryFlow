# InventoryFlow API

## Table of Contents
- [Overview](#overview)
- [Features](#-features)
- [Technical Pros](#️-technical-pros)
- [Business Logic and User Interaction Flow](#-business-logic-and-user-interaction-flow)
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

## 📈 Business Logic and User Interaction Flow

InventoryFlow is designed to model real-world inventory processes by defining clear roles and workflows for different user types. The core of the system revolves around the movement of products from suppliers to the warehouse (stock) and then out to customers.

```mermaid
graph LR
    subgraph Admin
        direction LR
        A[Admin]
    end

    subgraph Staff
        direction LR
        S[Staff]
    end

    subgraph Customer
        direction LR
        C[Customer]
    end

    subgraph Supplier
        direction LR
        SU[Supplier]
    end

    A -- Manages all data & users --> System
    S -- Manages inventory & orders --> System
    C -- Places orders & views products --> System
    SU -- Fulfills incoming orders --> System

    System -- Provides comprehensive dashboards --> A
    System -- Provides operational data --> S
    System -- Shows product catalog & order history --> C
    System -- Shows assigned orders & profile --> SU
```

### User Roles & Workflow

1.  **Admin**:
    -   **Role**: The superuser with complete oversight and control over the entire system.
    -   **Interactions**: Admins can manage user accounts (create, update, delete), view system-wide dashboards with analytics, and perform any action available to other roles. They are responsible for system health and high-level management.

2.  **Staff**:
    -   **Role**: The primary operators of the inventory system.
    -   **Interactions**: Staff members handle the day-to-day logistics. They are responsible for:
        -   Creating and managing `products` and `categories`.
        -   Recording `incoming orders` from suppliers, which adds to the `stock`.
        -   Processing `outgoing orders` for customers, which deducts from the `stock`.
        -   Managing `customer` and `supplier` records.
        -   Monitoring inventory levels and operational dashboards.

3.  **Customer**:
    -   **Role**: The end-consumer who purchases products.
    -   **Interactions**: Customers have a limited, focused view of the system. They can:
        -   Browse the `product` catalog.
        -   Place `outgoing orders` for products they wish to purchase.
        -   View their own order history and profile.

4.  **Supplier**:
    -   **Role**: The entity that provides products to replenish the inventory.
    -   **Interactions**: Suppliers interact with the system to manage their supply chain relationship. They can:
        -   View their own profile information.
        -   See the `incoming orders` that have been assigned to them.
        -   Update the status of their assigned orders (e.g., from `pending` to `shipped`).

### Core Logic Flow

The central logic connects these roles. A `Staff` member creates an `Incoming Order` from a `Supplier`. When this order is fulfilled, a `Stock` record is created or updated. A `Customer` then places an `Outgoing Order`, which consumes from that `Stock`. The `Admin` can oversee this entire lifecycle, from supply to sale, through the dashboard.

This model ensures a clear separation of duties and a logical flow of data that mirrors a real-world inventory management process.

## 🔐 Roles & Permissions

| Role     | Capabilities                                                   |
|----------|----------------------------------------------------------------|
| Admin    | Full access to all endpoints and data                          |
| Staff    | Manage inventory, suppliers, customers, and view dashboards    |
| Customer | Limited access: view products, place orders                    |
| Supplier | View own profile and incoming orders                           |



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
    Interactive Swagger API docs would be available at `http://localhost:8000\docs`

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

**Request**: `AuthRegister`
```json
{
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "password": "strongpassword123",
  "role": "customer",
  "phone": "123-456-7890",
  "address": "123 Main St"
}
```

**Response**: `User`
```json
{
  "id": 1,
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "role": "customer",
  "email": "john.doe@example.com"
}
```

**Errors**:
- `400 Bad Request`: Email already registered.

#### POST /auth/login
**Description**: Authenticates a user and returns JWT tokens.

**Request**: `AuthLogin`
```json
{
  "email": "john.doe@example.com",
  "password": "strongpassword123"
}
```

**Response**: `AuthResponse`
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

**Response**: `User`
```json
{
  "id": 1,
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "role": "customer",
  "email": "john.doe@example.com"
}
```

**Errors**:
- `401 Unauthorized`: Invalid token or user not found.

#### **Category Management**
---
#### POST /categories/create
**Description**: Creates a new product category. (Admin role required)

**Request**: `CategoryCreate`
```json
{
  "name": "Electronics",
  "description": "Gadgets and electronic devices"
}
```

**Response**: `CategoryResponse`
```json
{
  "id": 1,
  "name": "Electronics",
  "description": "Gadgets and electronic devices",
  "created_at": "2023-10-27T10:00:00Z",
  "updated_at": "2023-10-27T10:00:00Z"
}
```

#### GET /categories/
**Description**: Retrieves a list of all product categories. (Admin, Staff, Customer roles required)

**Response**: `List[CategoryResponse]`
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

#### GET /categories/{category_id}
**Description**: Retrieves a single category by its ID. (Admin, Staff, Customer roles required)

**Response**: `CategoryResponse`
```json
{
  "id": 1,
  "name": "Electronics",
  "description": "Gadgets and electronic devices",
  "created_at": "2023-10-27T10:00:00Z",
  "updated_at": "2023-10-27T10:00:00Z"
}
```

#### PUT /categories/{category_id}
**Description**: Updates an existing category. (Admin role required)

**Request**: `CategoryUpdate`
```json
{
  "name": "Consumer Electronics",
  "description": "Updated description for gadgets"
}
```

**Response**: `CategoryResponse`
```json
{
  "id": 1,
  "name": "Consumer Electronics",
  "description": "Updated description for gadgets",
  "created_at": "2023-10-27T10:00:00Z",
  "updated_at": "2023-10-27T10:05:00Z"
}
```

#### DELETE /categories/{category_id}
**Description**: Deletes a category by its ID. (Admin role required)

**Response**: `202 Accepted`

---
#### **Customer Management**
---
#### POST /customers/
**Description**: Creates a new customer. (Admin role required)

**Request**: `CustomerCreate`
```json
{
  "user_id": 1,
  "first_name": "Jane",
  "last_name": "Doe",
  "phone_number": "555-555-5555",
  "address": "456 Oak Ave"
}
```

**Response**: `CustomerResponse`
```json
{
  "id": 1,
  "user_id": 1,
  "first_name": "Jane",
  "last_name": "Doe",
  "phone_number": "555-555-5555",
  "address": "456 Oak Ave",
  "created_at": "2023-10-27T10:00:00Z",
  "updated_at": "2023-10-27T10:00:00Z"
}
```

#### GET /customers/
**Description**: Retrieves a list of all customers. (Admin, Staff roles required)

**Response**: `List[CustomerSummary]`
```json
[
  {
    "id": 1,
    "first_name": "Jane",
    "last_name": "Doe"
  }
]
```

#### GET /customers/{customer_id}
**Description**: Retrieves a single customer by ID. (Admin, Staff, Customer roles required)

**Response**: `CustomerResponse`
```json
{
  "id": 1,
  "user_id": 1,
  "first_name": "Jane",
  "last_name": "Doe",
  "phone_number": "555-555-5555",
  "address": "456 Oak Ave",
  "created_at": "2023-10-27T10:00:00Z",
  "updated_at": "2023-10-27T10:00:00Z"
}
```

#### PUT /customers/{customer_id}
**Description**: Updates a customer by ID. (Admin role required)

**Request**: `CustomerUpdate`
```json
{
  "phone_number": "555-555-5556"
}
```

**Response**: `CustomerResponse`
```json
{
  "id": 1,
  "user_id": 1,
  "first_name": "Jane",
  "last_name": "Doe",
  "phone_number": "555-555-5556",
  "address": "456 Oak Ave",
  "created_at": "2023-10-27T10:00:00Z",
  "updated_at": "2023-10-27T10:05:00Z"
}
```

#### DELETE /customers/{customer_id}
**Description**: Deletes a customer by ID. (Admin role required)

**Response**: `204 No Content`

---
#### **Dashboard**
---
#### GET /dashboard/
**Description**: Retrieves dashboard data. (Admin, Staff roles required)

**Response**: `DashboardResponse`
```json
{
  "user_overview": {
    "total_users": 100,
    "new_users_last_30_days": 5,
    "user_role_distribution": {
      "admin": 2,
      "staff": 10,
      "customer": 80,
      "supplier": 8
    }
  },
  "performance_metrics": {
    "inventory": {
      "total_products": 500,
      "total_categories": 10,
      "total_stock_quantity": 10000,
      "inventory_value": 500000.00
    },
    "orders": {
      "total_incoming_orders": 50,
      "total_outgoing_orders": 200,
      "total_incoming_value": 75000.00,
      "total_outgoing_value": 120000.00
    }
  },
  "recent_activity": {
    "recent_outgoing_orders": [
      {
        "id": 1,
        "customer_id": 1,
        "product_id": 1,
        "quantity": 2,
        "total_price": 2400,
        "status": "completed",
        "order_date": "2023-10-27T11:00:00Z"
      }
    ],
    "recent_user_registrations": [
      {
        "id": 1,
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe",
        "role": "customer",
        "email": "john.doe@example.com"
      }
    ]
  }
}
```

---
#### **Product Management**
---
#### POST /products/create
**Description**: Creates a new product. (Admin role required)

**Request**: `ProductCreate`
```json
{
  "name": "Laptop Pro",
  "description": "A high-end laptop",
  "price": 1200,
  "category_id": 1
}
```

**Response**: `ProductResponse`
```json
{
  "id": 1,
  "name": "Laptop Pro",
  "description": "A high-end laptop",
  "price": 1200,
  "category": {
    "id": 1,
    "name": "Electronics"
   },
  "created_at": "2023-10-27T10:10:00Z",
  "updated_at": "2023-10-27T10:10:00Z"
}
```

#### GET /products/
**Description**: Retrieves a list of all products. (Admin, Staff, Customer, Supplier roles required)

**Response**: `List[ProductSummary]`
```json
[
  {
    "id": 1,
    "name": "Laptop Pro"
  }
]
```

#### GET /products/{id}
**Description**: Retrieves a single product by its ID. (Admin, Staff, Customer, Supplier roles required)

**Response**: `ProductResponse`
```json
{
  "id": 1,
  "name": "Laptop Pro",
  "description": "A high-end laptop",
  "price": 1200,
  "category": {
    "id": 1,
    "name": "Electronics"
   },
  "created_at": "2023-10-27T10:10:00Z",
  "updated_at": "2023-10-27T10:10:00Z"
}
```

#### PUT /products/{id}
**Description**: Updates an existing product. (Admin role required)

**Request**: `ProductUpdate`
```json
{
  "price": 1150,
  "description": "An updated high-end laptop"
}
```

**Response**: `ProductResponse`
```json
{
  "id": 1,
  "name": "Laptop Pro",
  "description": "An updated high-end laptop",
  "price": 1150,
  "category": {
    "id": 1,
    "name": "Electronics"
   },
  "created_at": "2023-10-27T10:10:00Z",
  "updated_at": "2023-10-27T10:15:00Z"
}
```

#### DELETE /products/{id}
**Description**: Deletes a product by its ID. (Admin role required)

**Response**: `202 Accepted`

---
#### **Stock Management**
---
#### GET /stocks/
**Description**: Retrieves a list of all stock entries. (Admin, Staff roles required)

**Response**: `List[StockSummary]`
```json
[
  {
    "id": 1,
    "available_quantity": 50
  }
]
```

#### GET /stocks/{id}
**Description**: Retrieves a specific stock entry by its ID. (Admin, Staff roles required)

**Response**: `StockResponse`
```json
{
  "id": 1,
  "product": {
    "id": 1,
    "name": "Laptop Pro"
  },
  "batch_number": "BATCH001",
  "available_quantity": 50,
  "expiry_date": "2025-12-31T00:00:00Z",
  "created_at": "2023-10-27T10:20:00Z",
  "updated_at": "2023-10-27T10:20:00Z"
}
```

#### PATCH /stocks/{id}
**Description**: Manually updates the quantity of a stock entry. (Admin, Staff roles required)

**Request**: `StockUpdate`
```json
{
  "available_quantity": 45
}
```

**Response**: `StockResponse`
```json
{
  "id": 1,
  "product": {
    "id": 1,
    "name": "Laptop Pro"
  },
  "batch_number": "BATCH001",
  "available_quantity": 45,
  "expiry_date": "2025-12-31T00:00:00Z",
  "created_at": "2023-10-27T10:20:00Z",
  "updated_at": "2023-10-27T10:25:00Z"
}
```

---
#### **Incoming Order Management**
---
#### POST /incoming/
**Description**: Creates a new incoming order from a supplier and updates stock. (Admin, Staff roles required)

**Request**: `IncomingOrderCreate`
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

**Response**: `IncomingOrderResponse`
```json
{
  "id": 1,
  "supplier": {
    "id": 1,
    "name": "Supplier A"
  },
  "product": {
    "id": 1,
    "name": "Laptop Pro"
  },
  "batch_number": "BATCH001",
  "quantity": 50,
  "unit_cost": 800,
  "total_cost": 40000,
  "status": "pending",
  "supply_date": "2023-10-27T10:20:00Z",
  "created_at": "2023-10-27T10:20:00Z",
  "updated_at": "2023-10-27T10:20:00Z"
}
```

#### GET /incoming/
**Description**: Retrieves a list of all incoming orders. (Admin, Staff roles required)

**Response**: `List[IncomingOrderSummary]`
```json
[
  {
    "id": 1,
    "supplier_id": 1,
    "product_id": 1,
    "batch_number": "BATCH001",
    "quantity": 50,
    "total_cost": 40000,
    "status": "pending",
    "supply_date": "2023-10-27T10:20:00Z"
  }
]
```

#### GET /incoming/{id}
**Description**: Retrieves a specific incoming order by its ID. (Admin, Staff, Supplier roles required)

**Response**: `IncomingOrderResponse`
```json
{
  "id": 1,
  "supplier": {
    "id": 1,
    "name": "Supplier A"
  },
  "product": {
    "id": 1,
    "name": "Laptop Pro"
  },
  "batch_number": "BATCH001",
  "quantity": 50,
  "unit_cost": 800,
  "total_cost": 40000,
  "status": "pending",
  "supply_date": "2023-10-27T10:20:00Z",
  "created_at": "2023-10-27T10:20:00Z",
  "updated_at": "2023-10-27T10:20:00Z"
}
```

#### GET /incoming/me
**Description**: Retrieves all incoming orders for the current supplier. (Supplier role required)

**Response**: `List[IncomingOrderSummary]`
```json
[
  {
    "id": 1,
    "supplier_id": 1,
    "product_id": 1,
    "batch_number": "BATCH001",
    "quantity": 50,
    "total_cost": 40000,
    "status": "pending",
    "supply_date": "2023-10-27T10:20:00Z"
  }
]
```

#### PATCH /incoming/{id}
**Description**: Updates the status of an incoming order. (Admin, Staff, Supplier roles required)

**Request**: `IncomingOrderStatusUpdate`
```json
{
  "status": "completed"
}
```

**Response**: `IncomingOrderResponse`
```json
{
  "id": 1,
  "supplier": {
    "id": 1,
    "name": "Supplier A"
  },
  "product": {
    "id": 1,
    "name": "Laptop Pro"
  },
  "batch_number": "BATCH001",
  "quantity": 50,
  "unit_cost": 800,
  "total_cost": 40000,
  "status": "completed",
  "supply_date": "2023-10-27T10:20:00Z",
  "created_at": "2023-10-27T10:20:00Z",
  "updated_at": "2023-10-27T10:25:00Z"
}
```

---
#### **Outgoing Order Management**
---
#### POST /outgoing/
**Description**: Creates a new outgoing order for a customer and decreases stock. (Admin, Staff, Customer roles required)

**Request**: `OutgoingOrderCreate`
```json
{
  "customer_id": 1,
  "product_id": 1,
  "stock_id": 1,
  "quantity": 2,
  "order_date": "2023-10-27T11:00:00Z"
}
```

**Response**: `OutgoingOrderResponse`
```json
{
  "id": 1,
  "customer": {
    "id": 1,
    "first_name": "Jane",
    "last_name": "Doe"
  },
  "product": {
    "id": 1,
    "name": "Laptop Pro"
  },
  "quantity": 2,
  "unit_price": 1200,
  "total_price": 2400,
  "status": "pending",
  "order_date": "2023-10-27T11:00:00Z",
  "created_at": "2023-10-27T11:00:00Z",
  "updated_at": "2023-10-27T11:00:00Z"
}
```

#### GET /outgoing/
**Description**: Retrieves a list of all outgoing orders. (Admin, Staff roles required)

**Response**: `List[OutgoingOrderSummary]`
```json
[
  {
    "id": 1,
    "customer_id": 1,
    "product_id": 1,
    "quantity": 2,
    "total_price": 2400,
    "status": "pending",
    "order_date": "2023-10-27T11:00:00Z"
  }
]
```

#### GET /outgoing/{id}
**Description**: Retrieves a specific outgoing order by its ID. (Admin, Staff, Customer roles required)

**Response**: `OutgoingOrderResponse`
```json
{
  "id": 1,
  "customer": {
    "id": 1,
    "first_name": "Jane",
    "last_name": "Doe"
  },
  "product": {
    "id": 1,
    "name": "Laptop Pro"
  },
  "quantity": 2,
  "unit_price": 1200,
  "total_price": 2400,
  "status": "pending",
  "order_date": "2023-10-27T11:00:00Z",
  "created_at": "2023-10-27T11:00:00Z",
  "updated_at": "2023-10-27T11:00:00Z"
}
```

---
#### **Supplier Management**
---
#### POST /suppliers/
**Description**: Creates a new supplier. (Admin role required)

**Request**: `SupplierCreate`
```json
{
  "user_id": 2,
  "name": "Supplier B",
  "phone_number": "111-222-3333",
  "email": "supplier.b@example.com",
  "address": "789 Pine St"
}
```

**Response**: `SupplierResponse`
```json
{
  "id": 2,
  "user_id": 2,
  "name": "Supplier B",
  "phone_number": "111-222-3333",
  "email": "supplier.b@example.com",
  "address": "789 Pine St",
  "created_at": "2023-10-27T10:00:00Z",
  "updated_at": "2023-10-27T10:00:00Z"
}
```

#### GET /suppliers/
**Description**: Retrieves a list of all suppliers. (Admin, Staff roles required)

**Response**: `List[SupplierSummary]`
```json
[
  {
    "id": 1,
    "name": "Supplier A"
  },
  {
    "id": 2,
    "name": "Supplier B"
  }
]
```

#### GET /suppliers/me
**Description**: Retrieves the profile of the current supplier. (Supplier role required)

**Response**: `SupplierResponse`
```json
{
  "id": 1,
  "user_id": 1,
  "name": "Supplier A",
  "phone_number": "123-456-7890",
  "email": "supplier.a@example.com",
  "address": "123 Maple St",
  "created_at": "2023-10-27T10:00:00Z",
  "updated_at": "2023-10-27T10:00:00Z"
}
```

#### GET /suppliers/{supplier_id}
**Description**: Retrieves a supplier by ID. (Admin, Staff roles required)

**Response**: `SupplierResponse`
```json
{
  "id": 1,
  "user_id": 1,
  "name": "Supplier A",
  "phone_number": "123-456-7890",
  "email": "supplier.a@example.com",
  "address": "123 Maple St",
  "created_at": "2023-10-27T10:00:00Z",
  "updated_at": "2023-10-27T10:00:00Z"
}
```

#### PUT /suppliers/{supplier_id}
**Description**: Updates a supplier by ID. (Admin role required)

**Request**: `SupplierUpdate`
```json
{
  "phone_number": "123-456-7891"
}
```

**Response**: `SupplierResponse`
```json
{
  "id": 1,
  "user_id": 1,
  "name": "Supplier A",
  "phone_number": "123-456-7891",
  "email": "supplier.a@example.com",
  "address": "123 Maple St",
  "created_at": "2023-10-27T10:00:00Z",
  "updated_at": "2023-10-27T10:05:00Z"
}
```

#### DELETE /suppliers/{supplier_id}
**Description**: Deletes a supplier by ID. (Admin role required)

**Response**: `204 No Content`

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
