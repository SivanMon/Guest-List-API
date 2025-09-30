# 🎉 Guest List API - DevSecOps Final Project

**Course:** DevSecOps  
**Team Members:** Gili, Sivan, Sahar, Dvir  
**Presenters:** Sivan & Dvir

A modern, cloud-native Flask REST API for managing event guest lists, built with containerization, AWS integration, and comprehensive CI/CD automation.

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [API Endpoints](#-api-endpoints)
- [Development Workflow](#-development-workflow)
- [Local Development](#-local-development)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Docker Configuration](#-docker-configuration)
- [Environment Variables](#-environment-variables)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Team Contributions](#-team-contributions)

## 🎯 Project Overview

This project demonstrates end-to-end DevSecOps practices through a complete guest management system. The API serves as the backend for event management, handling guest registration, updates, and deletions with full CRUD operations.

**Key Features:**
- RESTful API with Flask
- DynamoDB integration for scalable data storage
- Docker containerization
- Automated testing with local DynamoDB
- GitHub Actions CI/CD pipeline
- Multi-environment deployment support
- Health checks and monitoring endpoints

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub API    │    │  GitHub Deploy   │    │   AWS Cloud     │
│   Repository    │    │   Repository     │    │                 │
│                 │    │                  │    │                 │
│  ┌───────────┐  │    │  ┌─────────────┐ │    │ ┌─────────────┐ │
│  │Flask API  │  │    │  │ Terraform   │ │    │ │    EKS      │ │
│  │Container  │  │────┼─▶│Infrastructure│ │────┼─▶│  Cluster    │ │
│  │           │  │    │  │             │ │    │ │             │ │
│  └───────────┘  │    │  └─────────────┘ │    │ └─────────────┘ │
│                 │    │                  │    │                 │
│  ┌───────────┐  │    │  ┌─────────────┐ │    │ ┌─────────────┐ │
│  │GitHub     │  │    │  │K8s Manifests│ │    │ │ DynamoDB    │ │
│  │Actions CI │  │────┼──│& Deployment │ │    │ │   Table     │ │
│  │           │  │    │  │             │ │    │ │             │ │
│  └───────────┘  │    │  └─────────────┘ │    │ └─────────────┘ │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🛠️ Tech Stack

**Backend & API:**
- **Flask** - Web framework
- **Python 3.11** - Programming language
- **Boto3** - AWS SDK for Python

**Database:**
- **AWS DynamoDB** - NoSQL database
- **DynamoDB Local** - For testing

**Infrastructure & Deployment:**
- **Docker** - Containerization
- **Kubernetes/EKS** - Orchestration
- **AWS Cloud** - Infrastructure
- **Terraform** - Infrastructure as Code

**CI/CD & Automation:**
- **GitHub Actions** - CI/CD pipeline
- **Docker Hub** - Container registry

## 🚀 API Endpoints

### Core Guest Management
```http
GET    /guests           # Get all guests
POST   /guests           # Add new guest
GET    /guests/{id}      # Get specific guest by seq_num
DELETE /guests/{id}      # Delete guest by seq_num
```

### System Health
```http
GET    /health           # Application health check
GET    /healthz          # Kubernetes readiness probe
GET    /readyz           # Kubernetes liveness probe
```

### Application Info
```http
GET    /api              # API information and configuration
GET    /                 # Frontend web interface
```

### Request/Response Examples

**Add Guest (POST /guests):**
```json
{
  "id": "12345",
  "firstname": "John",
  "surname": "Doe",
  "quantity": "2",
  "phone": "0541234567",
  "email": "john.doe@example.com"
}
```

**Response:**
```json
{
  "message": "Guest created successfully",
  "guest": {
    "seq_num": "uuid-generated-id",
    "id": "12345",
    "firstname": "John",
    "surname": "Doe",
    "quantity": "2",
    "phone": "0541234567",
    "email": "john.doe@example.com"
  }
}
```

## 🔄 Development Workflow

Our team follows a structured GitFlow approach:

```
┌─────────────────┐    ┌─────────────┐    ┌─────────────┐    ┌──────────────┐
│ Student Feature │    │             │    │             │    │              │
│    Branches     │────▶│     dev     │────▶│ Environment │────▶│     main     │
│                 │    │             │    │   Deploy    │    │  (Production) │
│ gili-feature-*  │    │ Integration │    │             │    │              │
│ sivan-feature-* │    │   Testing   │    │ dev/staging │    │   Deploy     │
│ sahar-feature-* │    │             │    │             │    │              │
│ dvir-feature-*  │    │             │    │             │    │              │
└─────────────────┘    └─────────────┘    └─────────────┘    └──────────────┘
```

**Branch Strategy:**
1. **Feature Branches:** `{student-name}-feature-{description}`
2. **Development:** `dev` - Integration and testing
3. **Production:** `main` - Stable releases

**Deployment Environments:**
- **gili, sivan, sahar, dvir** - Individual student environments
- **dev** - Shared development environment  
- **main** - Production environment

## 💻 Local Development

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- AWS CLI (optional)

### Setup Instructions

1. **Clone the repository:**
```bash
git clone https://github.com/SivanMon/Guest-List-API.git
cd Guest-List-API
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run with local DynamoDB:**
```bash
# Start DynamoDB Local (Docker)
docker run -d -p 8000:8000 amazon/dynamodb-local:latest

# Set environment variables
export DDB_ENDPOINT_URL=http://localhost:8000
export DDB_TABLE=guests-local
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=localtest
export AWS_SECRET_ACCESS_KEY=localtest

# Create table (use AWS CLI or boto3 script)
aws dynamodb create-table \
  --table-name guests-local \
  --attribute-definitions AttributeName=seq_num,AttributeType=S \
  --key-schema AttributeName=seq_num,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --endpoint-url http://localhost:8000

# Run the application
python guestlist-server.py
```

5. **Access the application:**
   - API: http://localhost:1111
   - Web Interface: http://localhost:1111/

## 🔄 CI/CD Pipeline

Our GitHub Actions workflow (`api-workflow.yml`) provides comprehensive testing and deployment:

### Pipeline Stages

1. **Build & Test:**
   - Checkout code from appropriate branch
   - Set up Docker Buildx
   - Install Python dependencies
   - Build Docker image with test tag

2. **Integration Testing:**
   - Start DynamoDB Local service
   - Create test table
   - Run API container with local DynamoDB
   - Execute comprehensive API tests:
     - Health check validation
     - GET /guests endpoint
     - POST /guests with validation
     - GET /guests/{id} retrieval
     - DELETE /guests/{id} cleanup

3. **Image Publishing:**
   - Login to Docker Hub
   - Tag images based on branch:
     - `main` → `latest` + `{sha7}`
     - `dev` → `dev`
     - `{student}-feature-*` → `{student}-feature-{sha7}`
   - Push to `sivanmonshi/guestlistapi` repository

4. **Deployment Triggers:**
   - **Dev Environment:** Triggered on push to `dev` or manual `dev` run
   - **Production:** Triggered on PR to `main` or manual `main` run
   - Cross-repository dispatch to `Guest-List-Deploy`

### Trigger Matrix

| API Repository Event | Branch/Input | Docker Tag | Deploy Repository Action | Deploy Environment | Terraform Operation |
|---------------------|-------------|------------|--------------------------|-------------------|-------------------|
| **Push** | `main` | `latest` + `{sha7}` | None | - | - |
| **Push** | `dev` | `dev` | `repository_dispatch:`<br/>`deploy_plan` | `dev` | `terraform plan` |
| **Pull Request** | → `main` | None | `repository_dispatch:`<br/>`deploy_apply` | `main` | `terraform apply` |
| **Manual Dispatch** | `main` | `latest` | `repository_dispatch:`<br/>`deploy_apply` | `main` | `terraform apply` |
| **Manual Dispatch** | `staging` | `dev` | `repository_dispatch:`<br/>`deploy_apply` | `staging` | `terraform apply` |
| **Manual Dispatch** | `dev` | `dev` | `repository_dispatch:`<br/>`deploy_plan` | `dev` | `terraform plan` |
| **Manual Dispatch** | `{student}-feature` | `{student}-feature-`<br/>`{sha7}` | None | Individual env | Manual deployment |

### Cross-Repository Communication

| API Trigger | Repository Dispatch Event | Deploy Workflow Trigger | Final Action |
|-------------|---------------------------|-------------------------|--------------|
| Push to `dev` | `deploy_plan` | `clean-terraform.yml` | Infrastructure planning |
| Manual `dev` run | `deploy_plan` | `clean-terraform.yml` | Infrastructure planning |
| Manual `staging` run | `deploy_apply` | `clean-terraform.yml` | Staging deployment |
| PR to `main` | `deploy_apply` | `clean-terraform.yml` | Production deployment |
| Manual `main` run | `deploy_apply` | `clean-terraform.yml` | Production deployment |

### Repository Dispatch Payload Structure

```json
{
  "event_type": "deploy_plan",
  "client_payload": {
    "environment": "dev"
  }
}
```

```json
{
  "event_type": "deploy_apply", 
  "client_payload": {
    "environment": "main"
  }
}
```

## 🐳 Docker Configuration

Our Docker setup is optimized for production deployment:

**Dockerfile Features:**
- Python 3.11 slim base image
- Optimized layer caching
- Health check integration
- Non-root user security
- Multi-stage build ready

**Health Checks:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:1111/health')" || exit 1
```

## 🔧 Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `AWS_REGION` | AWS region for DynamoDB | `us-east-1` |
| `DDB_TABLE` | DynamoDB table name | `GuestList-dev` |
| `DDB_ENDPOINT_URL` | DynamoDB endpoint (local dev) | `http://localhost:8000` |
| `AWS_ACCESS_KEY_ID` | AWS credentials | From secrets |
| `AWS_SECRET_ACCESS_KEY` | AWS credentials | From secrets |

## 🧪 Testing

### Automated Testing
The CI pipeline includes comprehensive API testing:
- Health endpoint validation
- CRUD operation testing
- Error handling verification
- Integration with local DynamoDB

### Manual Testing
```bash
# Health check
curl http://localhost:1111/health

# Get all guests
curl http://localhost:1111/guests

# Add new guest
curl -X POST http://localhost:1111/guests \
  -H "Content-Type: application/json" \
  -d '{
    "id": "12345",
    "firstname": "Test",
    "surname": "User",
    "quantity": "1",
    "phone": "0541234567",
    "email": "test@example.com"
  }'
```

## 🚀 Deployment

Deployment is handled through the companion repository `Guest-List-Deploy` using Terraform and Kubernetes:

1. **Code Push** → API repository
2. **CI/CD Success** → Docker image published
3. **Repository Dispatch** → Deploy repository triggered
4. **Terraform Apply** → AWS infrastructure provisioned
5. **Kubernetes Deploy** → Application deployed to EKS

## 👥 Team Contributions

**Project Architecture & Design:**
- **Gili:** Flask API architecture and DynamoDB integration
- **Sivan:** Docker containerization and GitHub Actions CI/CD
- **Sahar:** Frontend interface and API testing strategies
- **Dvir:** Environment management and deployment workflows

**Implementation Focus:**
- **All Members:** Collaborative development on core API functionality
- **Sivan & Dvir:** Project presentation and documentation

## 📈 Future Enhancements

- **Monitoring Integration:** Prometheus/Grafana metrics
- **Advanced Security:** API authentication and rate limiting
- **Database Optimization:** Query performance and indexing
- **Microservices:** Event sourcing and CQRS patterns

---

**Repository:** https://github.com/SivanMon/Guest-List-API  
**Deploy Repository:** https://github.com/SivanMon/Guest-List-Deploy  
**Docker Hub:** https://hub.docker.com/r/sivanmonshi/guestlistapi

For deployment instructions and infrastructure details, see the [Guest-List-Deploy](https://github.com/SivanMon/Guest-List-Deploy) repository.
