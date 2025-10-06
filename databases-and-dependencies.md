# Databases and Dependencies

## 1. Overview

Each Minishop service manages its own data store.  
This ensures loose coupling, data ownership, and independent scalability.  
No service directly accesses another service’s database; they communicate only through APIs.

---

## 2. Database Ownership

| Service | Database | Purpose |
|----------|-----------|----------|
| Auth | PostgreSQL | Stores user credentials, JWT metadata, and account verification flags. |
| Catalog | PostgreSQL | Manages product data such as name, description, price, and inventory. |
| Cart | Redis | Stores user carts temporarily for fast access and session caching. |
| Orders | PostgreSQL | Maintains order records, statuses, and relationships to users and products. |
| Payments | None (Mock) | Simulates payment processing through an external API. |
| Shipping | PostgreSQL | Stores shipment details, tracking data, and delivery statuses. |
| Notifications | None | Relies on external APIs for sending emails or messages. |
| Gateway | None | Stateless; only routes traffic between clients and internal services. |

---

## 3. Database Isolation Principles

1. Each service has full control of its own schema and migrations.  
2. No direct cross-service joins or queries are allowed.  
3. Data shared between services must flow through REST APIs or asynchronous messages.  
4. Services can choose storage based on their specific needs (for example, PostgreSQL for relational data, Redis for caching).  
5. Backups and restores are managed independently per service.

---

## 4. External Dependencies

| Dependency | Used By | Purpose |
|-------------|----------|----------|
| SMTP or Email API (SendGrid, Mailgun) | Notifications | Sends user registration, order, and shipping emails. |
| Payment Gateway (Stripe Sandbox or Mock API) | Payments | Processes or simulates payment transactions. |
| Kubernetes Cluster | All Services | Handles orchestration, scaling, and networking. |
| Helm and ArgoCD | DevOps Pipeline | Define and automate application deployment. |
| Prometheus and Grafana | All Services | Monitor metrics and visualize service health. |
| ELK Stack (Elasticsearch, Logstash, Kibana) | All Services | Centralized logging for debugging and audits. |
| GitHub Actions | DevOps | Runs automated CI/CD pipelines for build, test, and deploy. |
| Docker | All Services | Packages each service as an isolated, reproducible container image. |

---

## 5. Data Security

- Passwords and tokens are hashed or encrypted before storage.  
- Databases accept connections only within the internal network.  
- Role-based access controls are applied to PostgreSQL instances.  
- Backups and configuration secrets are stored securely.  
- All traffic between services and databases is encrypted in transit.

---

## 6. Outcome

This structure guarantees that each service remains autonomous and resilient.  
It also ensures that Minishop can scale horizontally while maintaining strong data security and clear ownership boundaries.
