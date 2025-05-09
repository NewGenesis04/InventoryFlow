# 📦 InventoryFlow – Inventory Management API

InventoryFlow is a modern, production-ready Inventory Management System built with **FastAPI** and **PostgreSQL**. It supports **role-based access**, **stock tracking**, **customer/supplier management**, and **automated email notifications** – all wrapped in a sleek, testable REST API.

Built with scalability, security, and developer experience in mind, InventoryFlow is ideal for small-to-medium businesses, dev demos, or as a base for more complex ERP systems.

---

## 🌟 Features

- ✅ **CRUD** operations for Products, Categories, Customers, and Suppliers  
- 📦 Track **stock**, incoming & outgoing orders  
- 🔐 **Authentication & Authorization** with JWT and role-based access  
- 📬 **Email notifications** to suppliers and customers  
- 📊 Admin-friendly **dashboard endpoints** with analytics  
- 🔍 **Filtering, searching**, and **pagination** for large datasets  
- 🔁 Automated **unit/integration testing** (Pytest)  
- 📄 Interactive **API docs** with Swagger (OpenAPI)  

---

## 🧠 System Overview

The system manages inventory by tracking products, stock levels, suppliers, and customers. Incoming and outgoing orders affect the stock accordingly. Admins can monitor stock flow, while customers and suppliers receive relevant email notifications.

### 📘 Core Entities

- **Category**
  - `id`, `name`
- **Product**
  - `id`, `name`, `category_id`, `quantity`, `price`, `created_at`
- **Stock**
  - `id`, `product_id`, `available_quantity`, `product_price`, `total_price`, `date_created`
- **Customer**
  - `id`, `first_name`, `last_name`, `email`, `phone`, `address`, `created_at`
- **Supplier**
  - `id`, `first_name`, `last_name`, `email`, `phone`, `address`, `created_at`
- **IncomingOrder**
  - `id`, `product_id`, `supplier_id`, `quantity`, `total_price`, `supply_date`
- **OutgoingOrder**
  - `id`, `product_id`, `customer_id`, `quantity`, `discount`, `total_price`, `order_date`

---

## 🔐 Roles & Permissions

| Role     | Capabilities                                                   |
|----------|----------------------------------------------------------------|
| Admin    | Full access to all endpoints and data                          |
| Staff    | Manage inventory, suppliers, customers, and view dashboards    |
| Customer | Limited access: view products, place orders                    |

---

## ⚙️ Tech Stack

- **Backend**: FastAPI (async, typed, clean)
- **Database**: PostgreSQL/MySQL
- **ORM**: SQLAlchemy 2.0 + Alembic
- **Auth**: JWT-based with OAuth2 flow
- **Email**: SendGrid (or SMTP fallback)
- **Testing**: Pytest
- **Deployment**: Docker,Render, Fly.io

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL/MySQL
- SMTP credentials