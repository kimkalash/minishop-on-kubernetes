# Minishop on Kubernetes

# Minishop — Business Requirements

## 1. Business Purpose

Project Name: Minishop  
Business Goal:  
To create a modular, microservices-based e-commerce platform that demonstrates how modern cloud applications are built, secured, and deployed at scale.

Business Intent:  
Minishop exists as both a learning lab and a reference architecture for building, deploying, and securing distributed systems. The system should simulate a real online shop where users can browse products, add them to a cart, place orders, and process payments — while showcasing strong backend design, automation, and security practices.

Business Value:
- Provides a hands-on example of secure cloud architecture for clients or recruiters.  
- Enables future expansion into a commercial SaaS or pentesting demonstration tool.  
- Serves as a teaching environment for DevOps pipelines, observability, and scalability.

---

## 2. Core Features (Functional Requirements)

| Category | Feature | Description |
|-----------|----------|-------------|
| User Management | Registration | Users can sign up with username, password, and email. |
|  | Login / Authentication | Users log in via JWT-based authentication. |
|  | Profile / Account | View and update profile, see order history. |
| Catalog | Product Management | Admins can add, update, or delete products. |
|  | Product Listing | Users can browse or search products. |
| Cart | Add / Remove / View Cart | Logged-in users can manage cart contents. |
| Orders | Checkout | Create orders from cart items. |
|  | Order Management | Users and admins can track orders. |
| Payments | Process Payments | Mock payment service for testing. |
| Shipping | Shipment Tracking | Update shipment status from warehouse to delivery. |
| Notifications | Email / SMS Alerts | Send confirmations for registration, order placed, order shipped. |
| Gateway / API | Unified Entry Point | Gateway routes external requests securely to the right service. |
| Admin Panel (optional) | Management UI | Optional front-end admin portal. |

---

## 3. Non-Functional Requirements (NFRs)

| Category | Requirement | Description |
|-----------|--------------|-------------|
| Security | Authentication and Authorization | All endpoints protected by JWTs and role-based access. |
|  | Data Encryption | Sensitive data such as passwords and tokens stored encrypted. |
|  | Audit Logging | User and system actions logged for traceability. |
| Performance | Scalability | Microservices independently scalable via Kubernetes. |
|  | Response Time | API endpoints should respond in under 300 ms under normal load. |
| Reliability | Fault Tolerance | Redis and PostgreSQL configured for recovery and redundancy. |
|  | Monitoring | Metrics collected via Prometheus and Grafana. |
| Maintainability | Modularity | Each service isolated with clear contracts. |
|  | Documentation | Self-documented APIs via Swagger or OpenAPI. |
| Deployability | CI/CD | Automated test, build, and deploy pipeline using GitHub Actions and ArgoCD. |
| Portability | Containerization | Every component packaged as a Docker image. |
| Compliance | Logging and Privacy | Logs anonymized; privacy-compliant design principles applied. |

---

Outcome:  
This document defines the foundation for Minishop’s entire system.  
All future architecture, data models, and DevOps workflows trace back to these requirements.

