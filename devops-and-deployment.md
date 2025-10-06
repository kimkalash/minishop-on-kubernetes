# DevOps and Deployment

## 1. Overview

This document describes how Minishop is built, tested, and deployed using modern DevOps practices.  
The goal is to ensure reliability, automation, and scalability across all environments.

---

## 2. Continuous Integration (CI)

### Tooling
- GitHub Actions handles automated builds and tests.  
- Each service includes a `Dockerfile` and `requirements.txt`.  
- Linting and unit tests run on every pull request.  

### Typical Workflow

1. A developer pushes code or opens a pull request.  
2. GitHub Actions runs:
   - Code quality checks (Black, isort, Pylama).  
   - Unit tests using pytest and httpx.  
   - Docker image build for the modified service.  
3. On success, the image is pushed to Docker Hub or GitHub Container Registry.  

### Example CI Job (simplified)

name: CI
on: [push, pull_request]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: 3.11
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest -v
      - name: Build Docker image
        run: docker build -t minishop/${{ github.event.repository.name }} .
3. Continuous Delivery (CD)
Tools
ArgoCD for GitOps-style deployment.

Helm for Kubernetes resource management.

Kubernetes for container orchestration and scaling.

Workflow
Each service has its own Helm chart in the /charts folder.

Once a CI build passes, the Docker image tag is updated in the Helm values file.

ArgoCD detects the change and automatically synchronizes it with the Kubernetes cluster.

Environments
Environment	Purpose	Deployment Type
Development	Local testing (Docker Compose or Minikube)	Manual
Staging	Pre-production validation	Automated (ArgoCD)
Production	Live environment	Automated with manual approval

4. Kubernetes Deployment
Each service runs as its own Kubernetes Deployment, with a corresponding Service for networking.
The API Gateway exposes the entire system externally through an Ingress controller.

Example Deployment (simplified)
yaml
Copy code
apiVersion: apps/v1
kind: Deployment
metadata:
  name: auth-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: auth-service
  template:
    metadata:
      labels:
        app: auth-service
    spec:
      containers:
        - name: auth-service
          image: minishop/auth-service:latest
          ports:
            - containerPort: 8000
          envFrom:
            - secretRef:
                name: auth-service-secrets
5. Observability and Logging
Tool	Purpose
Prometheus	Collects service metrics.
Grafana	Visualizes performance dashboards.
ELK Stack (Elasticsearch, Logstash, Kibana)	Centralized logging and search.
Alertmanager	Sends alerts for failures or threshold breaches.

Each service exports metrics endpoints compatible with Prometheus (for example, /metrics).

6. Secrets and Configuration
Environment variables are stored in .env files for local use.

In Kubernetes, secrets are managed using Secret objects and mounted securely into pods.

Sensitive values (JWT secrets, database credentials) are never stored in Git or Docker images.

Configuration follows the Twelve-Factor App methodology.

7. Backup and Recovery
PostgreSQL data is backed up using scheduled Kubernetes CronJobs.

Redis data is persisted with mounted volumes.

Application logs and metrics are archived using S3-compatible storage.

Disaster recovery is validated periodically using test restores.

8. Local Development Setup
Prerequisites
Docker and Docker Compose

Python 3.11+

Git

Steps
Clone the repository:

bash
Copy code
git clone https://github.com/kimkalash/minishop-on-kubernetes.git
cd minishop-on-kubernetes
Copy example environment file:

bash
Copy code
cp .env.example .env
Build and start services locally:

bash
Copy code
docker compose up --build
Access the system at:

arduino
Copy code
http://localhost:8000
9. Deployment Pipeline Summary
Stage	Tool	Description
Source Control	GitHub	Code versioning and collaboration.
Build	GitHub Actions	Runs automated builds and tests.
Package	Docker	Creates container images for each service.
Deploy	ArgoCD + Helm	Automates deployment to Kubernetes.
Monitor	Prometheus, Grafana	Observes system health and metrics.
Log	ELK Stack	Aggregates logs for analysis.

10. Outcome
This DevOps design ensures Minishop remains scalable, observable, and continuously deployable.
From commit to production, the process is automated, traceable, and secure, supporting a reliable cloud-native lifecycle.
