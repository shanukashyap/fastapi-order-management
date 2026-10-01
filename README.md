# FastAPI Order Management System

A backend Order Management System built using **FastAPI, Python, SQLAlchemy, SQLite, and Pydantic**.

The application provides APIs for creating products, viewing products, creating orders, viewing orders, and updating order status.

## Features

* Create products
* View all products
* Create customer orders
* View all orders
* View a specific order
* Update order status
* Server-side order total calculation
* Product existence validation
* Quantity validation
* Stock validation
* Automatic stock reduction after an order
* Order status workflow validation
* SQLite database
* Swagger UI documentation
* Pydantic request validation
* SQLAlchemy ORM

## Technology Stack

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Uvicorn
* Swagger UI

## Project Structure

```text
fastapi-order-management/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── exceptions.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone https://github.com/shanukashyap/fastapi-order-management.git
```

Move into the project:

```bash
cd fastapi-order-management
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI can be used to test all API endpoints.

## API Endpoints

| Method | Endpoint                    | Description          |
| ------ | --------------------------- | -------------------- |
| POST   | `/products`                 | Create a product     |
| GET    | `/products`                 | Get all products     |
| POST   | `/orders`                   | Create an order      |
| GET    | `/orders`                   | Get all orders       |
| GET    | `/orders/{order_id}`        | Get a specific order |
| PUT    | `/orders/{order_id}/status` | Update order status  |

## Product Creation

### Request

```json
{
  "name": "Laptop",
  "price": 50000,
  "stock": 10
}
```

The server creates the product and assigns its ID.

## Order Creation

### Request

```json
{
  "customer": "Urmil Kashyap",
  "items": [
    {
      "product_id": 1,
      "quantity": 1
    },
    {
      "product_id": 2,
      "quantity": 2
    }
  ]
}
```

The client does not provide the final order amount.

The server retrieves the product prices from the database and calculates the total.

For example:

```text
Laptop: ₹50,000 × 1 = ₹50,000
Mouse:  ₹1,200 × 2 = ₹2,400

Total = ₹52,400
```

This prevents the client from directly manipulating the order total.

## Order Status

Orders follow the following workflow:

```text
PLACED
   ↓
PROCESSING
   ↓
SHIPPED
   ↓
DELIVERED
```

Invalid status transitions are rejected by the API.

For example:

```text
PLACED → SHIPPED
```

is rejected because the order must first move to:

```text
PROCESSING
```

## Validation

The API validates:

### Product validation

* Product name must contain at least 2 characters.
* Product price must be greater than 0.
* Product stock cannot be negative.

### Order validation

* Customer name must be provided.
* At least one product must be included.
* Product ID must exist.
* Quantity must be greater than 0.
* Requested quantity cannot exceed available stock.

### Status validation

Only valid status transitions are allowed:

```text
PLACED → PROCESSING
PROCESSING → SHIPPED
SHIPPED → DELIVERED
```

## Stock Management

When an order is successfully created, the ordered quantity is automatically deducted from the product stock.

For example:

```text
Initial stock = 10

Ordered quantity = 2

Remaining stock = 8
```

## Error Handling

The API returns appropriate HTTP errors.

Example:

```text
404 Not Found
```

when a product or order does not exist.

Example:

```text
400 Bad Request
```

when there is insufficient stock or an invalid status transition.

## Database

The project uses SQLite.

The database contains:

* `products`
* `orders`
* `order_items`

SQLAlchemy is used as the ORM.

## Complete Order Flow

The complete application flow is:

```text
Create Product
      ↓
View Products
      ↓
Create Order
      ↓
Validate Products
      ↓
Validate Quantity
      ↓
Calculate Total on Server
      ↓
Reduce Stock
      ↓
Order = PLACED
      ↓
PROCESSING
      ↓
SHIPPED
      ↓
DELIVERED
```

## Testing

The complete API can be tested through:

* Swagger UI
* Postman

Recommended tests:

1. Create a product.
2. Create multiple products.
3. Get all products.
4. Create an order.
5. Verify server-calculated total.
6. Get all orders.
7. Get a specific order.
8. Change status from PLACED to PROCESSING.
9. Change status from PROCESSING to SHIPPED.
10. Change status from SHIPPED to DELIVERED.
11. Test nonexistent product.
12. Test invalid quantity.
13. Test insufficient stock.
14. Test invalid status transition.
15. Test nonexistent order.

## Learning Outcomes

This project demonstrates:

* FastAPI routing
* REST API development
* Pydantic validation
* SQLAlchemy ORM
* SQLite database integration
* Dependency injection
* HTTP status codes
* Exception handling
* Business logic validation
* Server-side calculations
* Inventory management
* Order lifecycle management
* API testing using Swagger UI/Postman

## Author

Urmil Kashyap

GitHub:

```text
https://github.com/shanukashyap
```

## Project Submission

GitHub Repository:

```text
ADD YOUR FINAL GITHUB REPOSITORY URL HERE
```

YouTube Demonstration:

```text
ADD YOUR YOUTUBE VIDEO URL HERE
```
