# System Architecture

## 1. Overview

Minishop is built as a collection of independent microservices.  
Each service is responsible for a specific business domain and communicates with others through HTTP APIs or internal events.  
This modular structure allows scalability, easier maintenance, and independent deployments.

---

## 2. Service Diagram

The diagram below shows the logical flow between services.

```text
                         +----------------------+
                         |      Auth Service    |
                         |  User accounts       |
                         |  JWT authentication  |
                         +----------+-----------+
                                    |
                                    v
                      +-------------------------------+
                      |          API Gateway          |
                      | Routes external requests to   |
                      | internal services securely.   |
                      +----+---------------+----------+
                           |               |
          +----------------+               +----------------+
          v                                                 v
+----------------------+                          +----------------------+
|   Catalog Service    |                          |    Cart Service      |
| - Product details    |                          | - User carts         |
| - Pricing, stock     |                          | - Redis cache        |
+----------+-----------+                          +----------+-----------+
           |                                               |
           v                                               v
+----------------------+                          +----------------------+
|    Orders Service    |------------------------->|   Payments Service   |
| - Checkout           |  payment status updates  | - Mock processor     |
| - Order tracking     |                          | - External API ready |
+----------+-----------+                          +----------------------+
           |
           v
+----------------------+
|   Shipping Service   |
| - Shipments          |
| - Tracking updates   |
+----------+-----------+
           |
           v
+----------------------+
| Notifications Service|
| - Email and SMS      |
| - Alerts and logs    |
+----------------------+


## 3. Service Roles and Responsibilities

| Service | Description |
|----------|--------------|
| Auth Service | Manages users, credentials, and authentication tokens. |
| Catalog Service | Stores product information and handles product queries. |
| Cart Service | Maintains user carts using Redis for fast operations. |
| Orders Service | Handles order creation, tracking, and coordination between other services. |
| Payments Service | Processes and confirms payments using a mock or external API. |
| Shipping Service | Creates and updates shipment records for completed orders. |
| Notifications Service | Sends emails or SMS alerts to users for account, order, and shipping events. |
| API Gateway | Routes and secures all incoming traffic to internal services. |

---

## 4. Communication Patterns

1. Each microservice exposes a REST API.  
2. The API Gateway routes external requests to the right service.  
3. Services communicate with each other using internal HTTP calls.  
4. Future versions can use asynchronous communication with message queues (e.g., RabbitMQ, Kafka).

---

## 5. Design Principles

| Principle | Description |
|------------|--------------|
| Single Responsibility | Each service focuses on one core business domain. |
| Database per Service | Each microservice owns and manages its own data store. |
| Statelessness | Services avoid maintaining user session state. |
| Fault Isolation | A failure in one service should not cascade to others. |
| API-First Design | Each service defines and documents APIs before implementation. |
| Observability | All services emit logs and metrics for monitoring and debugging. |

---

## 6. Deployment Model

- Each service is containerized using Docker.  
- Kubernetes manages service deployment, scaling, and networking.  
- Helm charts define configurations and dependencies.  
- ArgoCD provides GitOps-based continuous delivery.  
- GitHub Actions automates build, test, and deploy steps.

---

## 7. Outcome

This architecture ensures Minishop remains scalable, fault-tolerant, and maintainable.  
Each component can evolve independently while still working together as a unified platform.
