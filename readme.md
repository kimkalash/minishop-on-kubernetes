1. Business Requirements

Provide a cloud-native e-commerce platform running on Kubernetes.

Support a modular microservices architecture where each service is independently deployable.

Deliver a full shopping flow:

User authentication & authorization.

Product catalog browsing.

Cart management.

Order creation & tracking.

Payment processing.

Shipping management.

Notifications for key events (e.g., order confirmation).

Ensure scalability, resilience, and maintainability.

2. Functional Requirements
2.1 Authentication Service

Users can register with username, email, and password.

Users can login and receive a JWT token.

JWT token must be validated across services.

Manage email verification status.

2.2 Catalog Service

Admin can create, update, delete products.

Users can list and view products.

Products include id, name, description, price, stock.

2.3 Cart Service

Users can add items to cart.

Users can remove items or clear cart.

Cart persists per user in Redis.

Cart calculates total items and total price.

2.4 Orders Service

Users can create orders from cart.

Orders store user_id, status, total_price.

Orders can be updated (e.g., shipped, cancelled).

Users can list their orders.

2.5 Payments Service

Process payments (mock or external API).

Return success/failure status.

Link payments to orders.

2.6 Shipping Service

Manage shipping records tied to orders.

Update shipping status (pending, in transit, delivered).

2.7 Notifications Service

Send email or message when:

Order is placed.

Payment confirmed.

Shipping updated.

2.8 Gateway Service

Single entry point for client apps.

Routes requests to correct microservice.

3. Non-Functional Requirements

Scalability: Horizontal scaling in Kubernetes.

CI/CD: Automated builds/tests via GitHub Actions, GitOps via ArgoCD.

Security: JWT auth, secret management via Kubernetes Secrets.

Observability: Logging, monitoring (Prometheus/Grafana), tracing (OpenTelemetry).

Resilience: Services isolated; failures don’t crash the whole system.

Portability: Runs locally (Docker Compose) and in Kubernetes.

Testing: Unit + integration tests with coverage reports.

Documentation: Requirements, design, and API docs stored in repo.
