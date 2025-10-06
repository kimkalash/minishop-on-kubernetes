# Data Flow and API Contracts

## 1. Overview

This document describes how Minishop services communicate and exchange data.  
Each service exposes REST APIs for other services to consume.  
All inter-service communication is authenticated using JWT tokens issued by the Auth Service.

---

## 2. General Request Flow

1. The user registers or logs in through the Auth Service, which returns a JWT token.  
2. The user browses products from the Catalog Service.  
3. The user adds products to their cart using the Cart Service.  
4. The user checks out through the Orders Service.  
5. The Orders Service verifies user identity, retrieves cart items, and initiates payment.  
6. The Payments Service processes the payment and responds with a success or failure status.  
7. On success, the Orders Service records the order, triggers the Shipping Service, and sends notifications through the Notifications Service.

---

## 3. Service-to-Service Communication

### 3.1 Authentication

All internal API calls include an Authorization header:

Authorization: Bearer <JWT_TOKEN>

Token payload example:

```json
{
  "sub": "user_123",
  "username": "abdulakeem",
  "role": "customer",
  "exp": 1735689600
}
3.2 Catalog Service

Endpoint:
GET /catalog/products

Response Example:
[
  {
    "id": 1,
    "name": "Wireless Keyboard",
    "price": 49.99,
    "stock": 100
  }
]
3.3 Cart Service

Endpoints:
POST /cart/items – Add an item
GET /cart – Retrieve current user cart

Request Example:
{
  "product_id": 1,
  "quantity": 2
}
Response Example:
{
  "items": [
    {"product_id": 1, "quantity": 2, "price": 49.99}
  ],
  "total_items": 1,
  "total_price": 99.98
}
3.4 Orders Service

Endpoint:
POST /orders/checkout

Flow:

Validates JWT with Auth.

Fetches cart data from Cart Service.

Sends payment request to Payments Service.

Creates new order on success.

Notifies Shipping and Notifications Services.

Request Example:
{
  "user_id": 1,
  "payment_method": "credit_card"
}
Response Example:
{
  "order_id": "ORD-101",
  "status": "paid",
  "total": 99.98
}
3.5 Payments Service

Endpoint:
POST /payments/process

Request Example:
{
  "order_id": "ORD-101",
  "amount": 99.98,
  "method": "credit_card"
}
Response Example:
{
  "payment_id": "PAY-555",
  "status": "success",
  "timestamp": "2025-10-06T18:21:00Z"
}
3.6 Shipping Service

Endpoints:
POST /shipping/create – Create a shipment
GET /shipping/{order_id} – Check shipment status

Request Example:

{
  "order_id": "ORD-101",
  "address": "123 Main Street, St. John's",
  "carrier": "Canada Post"
}


Response Example:

{
  "order_id": "ORD-101",
  "tracking_id": "SHIP-888",
  "status": "in_transit"
}

3.7 Notifications Service

Endpoint:
POST /notifications/send

Request Example:

{
  "recipient": "user@example.com",
  "subject": "Order Confirmation",
  "body": "Your order ORD-101 has been placed successfully."
}


Response Example:

{
  "status": "sent",
  "timestamp": "2025-10-06T18:22:00Z"
}

4. Data Flow Summary
Step	Source	Destination	Purpose
1	User	Auth	Register or log in to get JWT token.
2	User	Catalog	Browse available products.
3	User	Cart	Add or remove products in the cart.
4	Orders	Cart	Retrieve cart data during checkout.
5	Orders	Payments	Request payment processing.
6	Orders	Shipping	Create shipment after payment success.
7	Orders	Notifications	Send order confirmation.
8	Shipping	Notifications	Send delivery or tracking updates.
5. Security and Validation

All requests require valid JWT authentication.

Only authorized roles can access admin or management endpoints.

Sensitive data such as passwords and payment details are never logged.

Services validate payloads using Pydantic schemas.

All inter-service traffic inside Kubernetes is restricted to internal networking.

6. Outcome

This document defines how services in Minishop exchange data and enforce consistency.
Each API is self-contained, and no service directly accesses another’s database.
This guarantees modularity, security, and predictable data flow across the platform.

---





