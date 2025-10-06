# DevOps and Deployment

## 1. Overview

This document describes how Minishop is built, tested, and deployed using modern DevOps practices.  
The goal is to ensure reliability, automation, and scalability across all environments.

---

## 2. Continuous Integration (CI)

### Tooling
- GitHub Actions handles automated builds and tests.  
- Each service includes a Dockerfile and requirements.txt.  
- Linting and unit tests run on every pull request.

### Typical Workflow
1. A developer pushes code or opens a pull request.  
2. GitHub Actions runs the following steps:  
   - Code quality checks (Black, isort, Pylama).  
   - Unit tests using pytest and httpx.  
   - Builds a Docker image for the modified service.  
3. On success, the image is pushed to Docker Hub or GitHub Container Registry.

### Example CI Job (simplified)
Name: CI  
Trigger: On push or pull request  

Steps:
- Checkout repository  
- Set up Python 3.11  
- Install dependencies from requirements.txt  
- Run unit tests  
- Build Docker image for the service  

---

## 3. Continuous Delivery (CD)

### Tools
- ArgoCD for GitOps-style deployment  
- Helm for Kubernetes resource management  
- Kubernetes for container orchestration and scaling  

### Workflow
1. Each service has its own Helm chart in the charts folder.  
2. Once a CI build passes, the Docker image tag is updated in the Helm values file.  
3. ArgoCD detects the change and automatically synchronizes it with the Kubernetes cluster.

### Environments

| Environment | Purpose | Deployment Type |
|--------------|----------|----------------|
| Development | Local testing (Docker Compose or Minikube) | Manual |
| Staging | Pre-production validation | Automated (ArgoCD) |
| Production | Live environment | Automated with manual approval |

---

## 4. Kubernetes Deployment

Each service runs as its own Kubernetes Deployment, with a corresponding Service for networking.  
The API Gateway exposes the system externally through an Ingress controller.

Example configuration (simplified):

- Deployment name: auth-service  
- Replicas: 2  
- Container image: minishop/auth-service:latest  
- Port: 8000  
- Environment variables loaded from Kubernetes Secrets  

---

## 5. Observability and Logging

| Tool | Purpose |
|------|----------|
| Prometheus | Collects service metrics |
| Grafana | Visualizes performance dashboards |
| ELK Stack (Elasticsearch, Logstash, Kibana) | Centralized logging and search |
| Alertmanager | Sends alerts for failures or threshold breaches |

Each service exposes a metrics endpoint compatible with Prometheus (for example, `/metrics`).

---

## 6. Secrets and Configuration

- Environment variables are stored in .env files for local use.  
- In Kubernetes, secrets are managed with Secret objects and mounted securely into pods.  
- Sensitive values such as JWT secrets and database credentials are never stored in Git or Docker images.  
- Configuration follows the Twelve-Factor App methodology.

---

## 7. Backup and Recovery

- PostgreSQL databases are backed up using scheduled Kubernetes CronJobs.  
- Redis data is persisted using mounted volumes.  
- Application logs and metrics are archived using S3-compatible storage.  
- Disaster recovery is tested periodically through restore simulations.

---

## 8. Local Development Setup

### Prerequisites
- Docker and Docker Compose  
- Python 3.11 or higher  
- Git

### Steps
1. Clone the repository  
   `git clone https://github.com/kimkalash/minishop-on-kubernetes.git`  
   `cd minishop-on-kubernetes`  
2. Copy the example environment file  
   `cp .env.example .env`  
3. Build and start the services locally  
   `docker compose up --build`  
4. Access the system at  
   `http://localhost:8000`

---

## 9. Deployment Pipeline Summary

| Stage | Tool | Description |
|--------|------|-------------|
| Source Control | GitHub | Code versioning and collaboration |
| Build | GitHub Actions | Automated build and testing |
| Package | Docker | Creates container images for each service |
| Deploy | ArgoCD and Helm | Automates deployment to Kubernetes |
| Monitor | Prometheus and Grafana | Observes system health and metrics |
| Log | ELK Stack | Aggregates logs for analysis |

---

## 10. Outcome

This DevOps design ensures Minishop remains scalable, observable, and continuously deployable.  
From commit to production, the process is automated, traceable, and secure, supporting a reliable cloud-native lifecycle.

