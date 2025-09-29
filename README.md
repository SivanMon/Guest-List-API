## 🎉 Guest List API

A production-ready Flask REST API for event guest management, built as our final DevSecOps project. This lightweight API handles guest registration with validation, integrates with DynamoDB for persistence, and includes a modern web interface.

**Team:** Gili, Sivan, Sahar & Dvir

---

## 🏗️ Project Architecture

### Core Components
- **Backend**: Flask REST API with comprehensive validation
- **Database**: AWS DynamoDB for scalable guest storage
- **Frontend**: Modern HTML/CSS/JS interface with real-time updates
- **Container**: Docker-ready with health checks
- **CI/CD**: GitHub Actions with automated testing

### Key Features
- ✅ Complete CRUD operations for guest management
- ✅ Israeli phone number validation
- ✅ Duplicate prevention by guest ID
- ✅ Real-time web dashboard
- ✅ Docker containerization
- ✅ Health monitoring endpoints
- ✅ Automated testing pipeline
- ✅ DynamoDB integration with local development support

---

## 🚀 Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/giligalili/Guest-List-API.git
cd Guest-List-API

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export AWS_REGION=us-east-1
export DDB_TABLE=guests-dev
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret

# Run the application
python guestlist-server.py
```

Access the application at `http://localhost:1111`

### Docker Deployment

```bash
# Build the image
docker build -t giligalili/guestlistapi:latest .

# Run with environment variables
docker run -p 1111:1111 \
  -e AWS_REGION=us-east-1 \
  -e DDB_TABLE=guests-dev \
  -e AWS_ACCESS_KEY_ID=your-key \
  -e AWS_SECRET_ACCESS_KEY=your-secret \
  giligalili/guestlistapi:latest
```

---

## 📚 API Documentation

### Base Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serves the web interface |
| `/api` | GET | API information and health |
| `/health` | GET | Application health status |
| `/healthz` | GET | Kubernetes health probe |
| `/readyz` | GET | Kubernetes readiness probe |

### Guest Management

#### Get All Guests
```http
GET /guests
```
Returns all guests in the system as a dictionary keyed by `seq_num`.

**Response Example:**
```json
{
  "uuid-1": {
    "seq_num": "uuid-1",
    "id": "JD2025",
    "firstname": "John",
    "surname": "Doe",
    "quantity": "2",
    "phone": "0541234567",
    "email": "john@example.com"
  }
}
```

#### Add New Guest
```http
POST /guests
Content-Type: application/json

{
  "id": "JD2025",
  "firstname": "John",
  "surname": "Doe",
  "quantity": "2",
  "phone": "0541234567",
  "email": "john@example.com"
}
```

**Validation Rules:**
- `id`: Required, 5-20 digits
- `firstname`, `surname`, `email`: Required strings
- `quantity`: Required positive integer
- `phone`: Israeli format (10 digits starting with 0)

**Success Response (201):**
```json
{
  "message": "Guest created successfully",
  "guest": {
    "seq_num": "generated-uuid",
    "id": "JD2025",
    "firstname": "John",
    "surname": "Doe",
    "quantity": "2",
    "phone": "0541234567",
    "email": "john@example.com"
  }
}
```

#### Get Specific Guest
```http
GET /guests/{seq_num}
```

#### Delete Guest
```http
DELETE /guests/{seq_num}
```

### Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request (validation errors)
- `404`: Not Found
- `409`: Conflict (duplicate guest)
- `500`: Internal Server Error

---

## 🔧 Development Details

### File Structure
```
.
├── guestlist-server.py     # Main Flask application
├── index.html              # Web interface
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container definition
├── api-workflow.yml       # CI/CD pipeline
└── README.md              # This file
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AWS_REGION` | AWS region for DynamoDB | `us-east-1` |
| `DDB_TABLE` | DynamoDB table name | `guests-dev` |
| `DDB_ENDPOINT_URL` | DynamoDB endpoint (local dev) | None |
| `AWS_ACCESS_KEY_ID` | AWS credentials | Required |
| `AWS_SECRET_ACCESS_KEY` | AWS credentials | Required |

### Database Schema

**DynamoDB Table Structure:**
- **Primary Key**: `seq_num` (String) - UUID4 generated per guest
- **Attributes**:
  - `id`: User-provided guest identifier
  - `firstname`: Guest first name
  - `surname`: Guest last name
  - `quantity`: Number of people in the party
  - `phone`: Israeli phone number
  - `email`: Contact email

### Local DynamoDB Development

For local testing, the CI pipeline uses DynamoDB Local:

```bash
# Start DynamoDB Local
docker run -p 8000:8000 amazon/dynamodb-local:latest

# Set local endpoint
export DDB_ENDPOINT_URL=http://localhost:8000
```

---

## 🧪 Testing & CI/CD

### Complete GitHub Actions Workflow

Our comprehensive CI/CD pipeline (`api-workflow.yml`) implements a full test-build-deploy cycle:

#### **Workflow Triggers**
```yaml
on:
  push:
    branches: [ dev, staging, '*-feature' ]  # All feature branches
  pull_request:
    branches: [ main ]                       # PRs to main
```

#### **Pipeline Architecture**

**1. Environment Setup & Services**
```yaml
services:
  dynamodb:
    image: amazon/dynamodb-local:latest
    ports: [8000:8000]
    options: --health-cmd="curl -s http://localhost:8000/shell/ || exit 0"
```

- **OS**: Ubuntu latest with Python 3.12
- **DynamoDB Local**: Containerized database for isolated testing
- **Docker Buildx**: Advanced build features and caching
- **Health Checks**: Service readiness validation with retries

**2. Dependency Management**
```bash
# Python dependencies for testing utilities
pip install -r requirements.txt

# System utilities for API testing
sudo apt-get install -y jq  # JSON processing for API responses
```

**3. Docker Image Building**
```bash
docker build -t $DOCKERHUB_USER/$IMAGE_NAME:test .
```
- Builds test image before running any tests
- Uses repository secrets for Docker Hub credentials
- Separate test and production image tags

**4. DynamoDB Table Creation**
Our pipeline creates isolated test tables dynamically:
```python
# Embedded Python script in workflow
table = os.environ["DDB_TABLE"]  # guests-ci-{github.run_id}
ddb.create_table(
    TableName=table,
    AttributeDefinitions=[{"AttributeName": "seq_num", "AttributeType": "S"}],
    KeySchema=[{"AttributeName": "seq_num", "KeyType": "HASH"}],
    BillingMode="PAY_PER_REQUEST"
)
```
- **Unique Tables**: Each run gets isolated table (`guests-ci-{run_id}`)
- **Schema Validation**: Ensures table structure matches production
- **Readiness Waiting**: 30-iteration loop with 200ms intervals

**5. Container Integration Testing**
```bash
docker run -d \
  --name guestlist-test \
  --add-host=host.docker.internal:host-gateway \
  -p 1111:1111 \
  -e AWS_REGION="${AWS_REGION}" \
  -e DDB_TABLE="${DDB_TABLE}" \
  -e DDB_ENDPOINT_URL="http://host.docker.internal:8000" \
  $DOCKERHUB_USER/$IMAGE_NAME:test
```

**Container Configuration:**
- **Network Bridge**: `host.docker.internal` for DynamoDB Local access
- **Environment Variables**: Full AWS and DynamoDB configuration
- **Health Monitoring**: 40-iteration startup validation with curl
- **Failure Handling**: Container logs on health check failure

### Comprehensive API Test Suite

**6. Endpoint Validation Sequence**

**Health Check Validation:**
```bash
# Debug endpoint check
curl -fsS http://127.0.0.1:1111/api || true

# Primary health validation  
code=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:1111/guests)
if [ "$code" = "200" ]; then
  echo "✓ GET /guests passed"
else
  echo "✗ GET /guests failed (HTTP $code)"
  docker logs guestlist-test
  exit 1
fi
```

**Complete CRUD Testing:**

**POST /guests - Guest Creation:**
```bash
TEST_ID="111111111"
resp=$(curl -s -w "\n%{http_code}" -X POST http://127.0.0.1:1111/guests \
  -H "Content-Type: application/json" \
  -d '{
    "firstname": "CI",
    "surname": "Test", 
    "quantity": "2",
    "phone": "0541234567",
    "email": "ci@test.com",
    "id": "'${TEST_ID}'"
  }')

code=$(echo "$resp" | tail -1)
body=$(echo "$resp" | head -n -1)

# Parse seq_num for subsequent tests
seq_num=$(echo "$body" | jq -r '.guest.seq_num // empty')
echo "seq_num=$seq_num" >> $GITHUB_OUTPUT
```

**GET /guests/{id} - Individual Retrieval:**
```bash
SEQ='${{ steps.post.outputs.seq_num }}'
code=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:1111/guests/$SEQ")
```

**DELETE /guests/{id} - Guest Removal:**
```bash
code=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "http://127.0.0.1:1111/guests/$SEQ")
if [ "$code" = "200" ] || [ "$code" = "204" ]; then
  echo "✓ DELETE /guests/$SEQ passed"
fi
```

**Test Features:**
- **Response Validation**: HTTP status codes and JSON parsing
- **Data Flow Testing**: POST → GET → DELETE sequence
- **Error Handling**: Container logs on failure
- **Clean State**: Each test run starts fresh

### Advanced Docker Build & Push Strategy

**7. Environment-Based Tagging**
```bash
branch="${GITHUB_REF_NAME}"
sha7="${GITHUB_SHA::7}"

case "$branch" in
  main)    tag="latest" ;;
  staging) tag="staging" ;;
  dev)     tag="dev" ;;
  sivan-feature*|dvir-feature*|gili-feature*|sahar-feature*)
    prefix="${branch%%-*}"   # Extract student name
    tag="${prefix}-feature-${sha7}"
    ;;
  *) tag="dev" ;;
esac
```

**Tag Strategy:**
- **Production**: `latest` (main branch)
- **Environments**: `dev`, `staging` (fixed tags)
- **Feature Branches**: `{student}-feature-{sha7}` (unique per commit)
- **Fallback**: Default to `dev` for unknown branches

**8. Multi-Registry Push with Caching**
```yaml
- name: Push image to Docker Hub
  uses: docker/build-push-action@v6
  with:
    context: .
    push: true
    tags: |
      giligalili/guestlistapi:${{ steps.envtag.outputs.tag }}
      ${{ github.ref_name == 'main' && format('giligalili/guestlistapi:{0}', steps.envtag.outputs.sha7) || '' }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
    provenance: mode=max
```

**Push Strategy:**
- **All Branches**: Push with computed environment tag
- **Main Branch Only**: Additional SHA-based tag for version tracking
- **GitHub Actions Cache**: Build layer caching for faster builds
- **Provenance**: Security attestation and supply chain verification

### Pipeline Security & Best Practices

**Container Cleanup:**
```bash
- name: Stop test container (always)
  if: always()  # Runs even on failure
  run: |
    docker logs guestlist-test || true
    docker stop guestlist-test || true  
    docker rm guestlist-test || true
```

**Environment Isolation:**
- **Unique Table Names**: Prevents test conflicts
- **Local DynamoDB**: No impact on production data
- **Containerized Testing**: Isolated runtime environment
- **Cleanup Guarantees**: Resources cleaned up on success/failure

### CI/CD Integration with Deployment Pipeline

**Cross-Repository Workflow:**

1. **Code Development** (This Repository):
   ```
   Feature Branch (gili-feature) → API Workflow
   ├── Test with DynamoDB Local
   ├── Build & Push Docker Image: giligalili/guestlistapi:gili-feature-abc1234
   └── Ready for deployment
   ```

2. **Infrastructure Deployment** ([Deploy Repository](https://github.com/giligalili/Guest-List-Deploy)):
   ```
   Manual Trigger: environment=gili, action=apply
   ├── Queries Docker Hub for latest gili-feature-* tag
   ├── Deploys EKS cluster with resolved image
   └── Health validates deployed application
   ```

**Deployment Flow:**
```bash
# Developer workflow
git push origin gili-feature  # Triggers API workflow
# Wait for green build
# Navigate to deploy repository
# Trigger deployment workflow manually with environment=gili
```

**Image Tag Synchronization:**
- API workflow creates: `gili-feature-{short-sha}`
- Deploy workflow finds: Latest `gili-feature-*` tag via Docker Hub API
- Automatic resolution ensures latest feature code is deployed

### Branch Strategy & Deployment

**Trigger Patterns:**
```yaml
Feature Development:
  sivan-feature* → sivan-feature-{sha7}
  dvir-feature*  → dvir-feature-{sha7}  
  gili-feature*  → gili-feature-{sha7}
  sahar-feature* → sahar-feature-{sha7}

Environment Branches:
  dev     → dev
  staging → staging
  main    → latest + {sha7}
```

**Integration Points:**
- **Development**: Feature branches test in isolation
- **Integration**: PR validation to main branch
- **Deployment**: Environment branches trigger deployment pipeline
- **Production**: Main branch creates production-ready images

### Test Coverage & Quality Gates

**Comprehensive Validation:**
- ✅ **Service Health**: Container startup and health endpoints
- ✅ **Database Connectivity**: DynamoDB Local integration
- ✅ **API Functionality**: Complete CRUD operations
- ✅ **Data Validation**: Input validation and error handling
- ✅ **Response Format**: JSON structure and status codes
- ✅ **State Management**: Sequential operations (POST→GET→DELETE)
- ✅ **Container Integration**: Network and environment configuration

**Quality Assurance:**
- **Zero-downtime Testing**: Tests run in isolated environment
- **Realistic Conditions**: Container-based testing matches production
- **Comprehensive Logging**: Full container logs on failure
- **Fail-fast Strategy**: Stop pipeline immediately on test failure

---

## 🖥️ Web Interface

The included web interface (`index.html`) provides:

- **Real-time Guest Management**: Add, view, and delete guests
- **Statistics Dashboard**: Live count of guests and total people
- **Form Validation**: Client-side validation matching API rules
- **Responsive Design**: Mobile-friendly interface
- **API Information**: Built-in endpoint documentation

### Interface Features

- Modern gradient design with card-based layout
- Real-time statistics (total guests, total people)
- Form validation with immediate feedback
- Bulk operations (clear all guests)
- API endpoint information display
- Mobile-responsive design

---

## 🐳 Docker Configuration

### Multi-stage Build Optimization

Our Dockerfile uses Python 3.11 slim for minimal image size:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY guestlist-server.py index.html ./
EXPOSE 1111
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:1111/health')" || exit 1
CMD ["python", "guestlist-server.py"]
```

### Health Monitoring

Built-in health checks for container orchestration:
- **Health Check**: `/health` endpoint with guest count
- **Liveness Probe**: `/healthz` for basic service availability
- **Readiness Probe**: `/readyz` for dependency validation

---

## 🏃‍♀️ Performance Considerations

### Scalability Features

- **DynamoDB**: Auto-scaling NoSQL database
- **Stateless Design**: Containers can be horizontally scaled
- **Connection Pooling**: Efficient AWS SDK usage
- **Minimal Dependencies**: Fast startup times

### Resource Usage

- **Memory**: ~128MB base usage
- **CPU**: Minimal load for typical guest list sizes
- **Storage**: DynamoDB handles persistence
- **Network**: Optimized for cloud deployment

---

## 🔐 Security Features

### Input Validation
- Strict regex patterns for phone numbers and IDs
- SQL injection prevention (NoSQL backend)
- XSS protection through input sanitization
- CORS handling for web interface

### AWS Integration
- IAM role-based access control
- Encrypted data at rest (DynamoDB)
- VPC deployment support
- Secret management through environment variables

---

---

## 🔄 API Repository CI/CD Pipeline

### Overview
Our API repository implements a complete CI/CD pipeline that automatically builds, tests, and publishes Docker images based on branch patterns and triggers.

### Workflow File: `api-workflow.yml`

**Name**: "Build and Test API (Local DynamoDB)"

**Repository**: [Guest-List-API](https://github.com/giligalili/Guest-List-API)

### Trigger Strategy
```yaml
on:
  push:
    branches: [ dev, staging, '*-feature' ]  # All dev, staging, and feature branches
  pull_request:
    branches: [ main ]                       # PRs targeting main branch
```

**Trigger Logic:**
- **Feature Development**: Any branch matching `*-feature` pattern
- **Environment Branches**: `dev` and `staging` branches  
- **Integration Testing**: Pull requests to `main` branch
- **No Automatic Main**: Main branch deployments handled by deployment repository

### Pipeline Stages

#### 1. **Environment & Service Setup**
- **OS**: Ubuntu latest with Python 3.12
- **DynamoDB Local**: Containerized database on port 8000
- **Docker Buildx**: Advanced building capabilities
- **System Tools**: jq for JSON processing

#### 2. **Test Database Preparation**
- **Unique Table Names**: `guests-ci-{github.run_id}` for isolation
- **Schema Creation**: Matches production DynamoDB structure
- **Health Waiting**: Ensures table is active before testing

#### 3. **Application Testing**
- **Docker Build**: Creates test image tagged as `:test`
- **Container Deployment**: Runs with DynamoDB Local connection
- **Health Validation**: 40-attempt startup verification
- **API Testing**: Complete CRUD operation validation

#### 4. **Docker Registry Publishing**
- **Environment-based Tagging**: Branch name determines image tag
- **Multi-platform Push**: Publishes to Docker Hub
- **GitHub Actions Caching**: Optimizes build performance

### Image Tagging Strategy

Based on the actual workflow logic:

```bash
case "$branch" in
  main)    tag="latest" ;;
  staging) tag="staging" ;;  
  dev)     tag="dev" ;;
  sivan-feature*|dvir-feature*|gili-feature*|sahar-feature*)
    prefix="${branch%%-*}"                    # Extract: sivan, dvir, gili, sahar
    tag="${prefix}-feature-${sha7}"           # Result: gili-feature-abc1234
    ;;
  *) tag="dev" ;;                            # Fallback for other branches
esac
```

**Published Images:**
- `giligalili/guestlistapi:latest` ← main branch
- `giligalili/guestlistapi:staging` ← staging branch  
- `giligalili/guestlistapi:dev` ← dev branch
- `giligalili/guestlistapi:gili-feature-abc1234` ← gili-feature branch
- `giligalili/guestlistapi:sivan-feature-def5678` ← sivan-feature branch
- etc.

**Special Main Branch Handling:**
```yaml
tags: |
  giligalili/guestlistapi:${{ steps.envtag.outputs.tag }}
  ${{ github.ref_name == 'main' && format('giligalili/guestlistapi:{0}', steps.envtag.outputs.sha7) || '' }}
```
Main branch gets both `latest` AND a SHA-specific tag for version tracking.

### Integration with Deployment Pipeline

The API CI/CD connects with the deployment repository:

1. **API Repository** builds and pushes images with predictable tags
2. **Deploy Repository** queries Docker Hub API to find latest feature images
3. **Deployment** uses resolved image tags for Kubernetes deployment

**Example Flow:**
```
Developer pushes to gili-feature branch
  ↓
API Workflow triggers
  ↓  
Tests pass, image built: giligalili/guestlistapi:gili-feature-a1b2c3d
  ↓
Image pushed to Docker Hub  
  ↓
Developer triggers deployment workflow with environment=gili
  ↓
Deploy workflow queries Docker Hub for latest gili-feature-* tag
  ↓
Kubernetes deployment uses giligalili/guestlistapi:gili-feature-a1b2c3d
```

### Quality Gates

**Before Publishing:**
- ✅ All unit tests must pass
- ✅ DynamoDB integration tests must succeed
- ✅ Container health checks must validate
- ✅ API endpoints must respond correctly

**On Failure:**
- 🚫 No image is published
- 📋 Container logs are captured for debugging
- ⚠️ Pipeline fails with clear error messages

---

## 🚀 Deployment

This API is designed for cloud deployment. Check out our companion repository:
[Guest-List-Deploy](https://github.com/giligalili/Guest-List-Deploy) for Terraform-based Kubernetes deployment on AWS EKS.

### Available Images

Docker images are automatically built and pushed to:
`docker.io/giligalili/guestlistapi`

Tags available:
- `latest`: Production builds from main branch
- `dev`: Development builds
- `staging`: Staging environment builds
- `{student}-feature-{sha}`: Feature branch builds

---

## 📄 License

This project was created as part of a DevSecOps course final project.

---

## 🐛 Troubleshooting

### Common Issues

**Connection to DynamoDB fails:**
- Verify AWS credentials are set correctly
- Check DynamoDB table exists in specified region
- Ensure IAM permissions include DynamoDB access

**Docker container won't start:**
- Check all required environment variables are provided
- Verify AWS credentials have DynamoDB permissions
- Check container logs: `docker logs <container-name>`

**CI pipeline failures:**
- Ensure Docker Hub credentials are set in repository secrets
- Verify branch naming follows the pattern for feature builds
- Check DynamoDB Local service health in Actions logs

### Support

For issues or questions about this project, please open an issue in the GitHub repository or contact any team member.
