# ChatPPT Docker & CI/CD Deployment Guide

Complete guide for containerizing and deploying ChatPPT using Docker, Kubernetes, and CI/CD pipelines.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Docker Setup](#docker-setup)
- [Docker Compose](#docker-compose)
- [Kubernetes Deployment](#kubernetes-deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Environment Configuration](#environment-configuration)
- [Production Deployment](#production-deployment)

---

## 🚀 Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+ (optional)
- Kubernetes 1.24+ (for K8s deployment)
- Git

### Build and Run (Fastest)

```bash
# Build CPU version
docker build -f Dockerfile.cpu -t chatppt:latest-cpu .

# Run container
docker run -p 7860:7860 \
  -e OPENAI_API_KEY=your_key_here \
  chatppt:latest-cpu

# Access at http://localhost:7860
```

---

## 🐳 Docker Setup

### Available Docker Images

We provide three Dockerfile variants:

1. **Dockerfile.cpu** - CPU-only version (recommended for most users)
   - Smaller image size (~2GB)
   - Faster build time
   - No GPU required

2. **Dockerfile.gpu** - NVIDIA GPU support
   - CUDA 12.1 support
   - Larger image size (~5GB)
   - Requires NVIDIA GPU

3. **Dockerfile** - Standard version with auto-detection
   - Auto-detects GPU availability
   - Good for development

### Building Images

#### Using Build Scripts (Recommended)

**Linux/Mac:**
```bash
# Make script executable
chmod +x build-docker.sh

# Build CPU version
./build-docker.sh --type cpu

# Build GPU version
./build-docker.sh --type gpu

# Build both
./build-docker.sh --type all --version 1.0.0

# Build and push to registry
./build-docker.sh --type cpu --registry ghcr.io/username/chatppt --push
```

**Windows:**
```cmd
REM Build CPU version
build-docker.bat --type cpu

REM Build GPU version
build-docker.bat --type gpu

REM Build with custom version
build-docker.bat --type cpu --version 1.0.0
```

#### Manual Build

```bash
# CPU version
docker build -f Dockerfile.cpu -t chatppt:latest-cpu .

# GPU version
docker build -f Dockerfile.gpu -t chatppt:latest-gpu .

# With build arguments
docker build \
  -f Dockerfile.cpu \
  -t chatppt:1.0.0-cpu \
  --build-arg VERSION=1.0.0 \
  .
```

### Running Containers

#### Basic Run

```bash
# CPU version
docker run -p 7860:7860 chatppt:latest-cpu

# GPU version (requires --gpus flag)
docker run -p 7860:7860 --gpus all chatppt:latest-gpu
```

#### With Environment Variables

```bash
docker run -p 7860:7860 \
  -e OPENAI_API_KEY=${OPENAI_API_KEY} \
  -e AZURE_OPENAI_API_KEY=${AZURE_OPENAI_API_KEY} \
  -e AZURE_OPENAI_ENDPOINT=${AZURE_OPENAI_ENDPOINT} \
  chatppt:latest-cpu
```

#### With Volumes (Persistent Data)

```bash
docker run -p 7860:7860 \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/images:/app/images \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/models:/app/models \
  -e OPENAI_API_KEY=${OPENAI_API_KEY} \
  chatppt:latest-cpu
```

#### Detached Mode

```bash
docker run -d \
  --name chatppt \
  -p 7860:7860 \
  -v $(pwd)/output:/app/output \
  -e OPENAI_API_KEY=${OPENAI_API_KEY} \
  --restart unless-stopped \
  chatppt:latest-cpu
```

### Container Management

```bash
# View logs
docker logs chatppt

# Follow logs
docker logs -f chatppt

# Stop container
docker stop chatppt

# Start container
docker start chatppt

# Remove container
docker rm chatppt

# View running containers
docker ps

# Execute command in container
docker exec -it chatppt bash
```

---

## 🐳 Docker Compose

### Quick Start

```bash
# Copy environment file
cp .env.example .env

# Edit .env with your API keys
nano .env

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Configuration

The `docker-compose.yml` file includes:
- Automatic volume mounting
- Environment variable loading from `.env`
- Network configuration
- Health checks
- Restart policies

### GPU Support with Docker Compose

To enable GPU support, edit `docker-compose.yml` and uncomment the GPU service section:

```yaml
# Uncomment this section for GPU support
chatppt-gpu:
  build:
    context: .
    dockerfile: Dockerfile.gpu
  runtime: nvidia
  # ... rest of configuration
```

Then run:
```bash
docker-compose up -d chatppt-gpu
```

---

## ☸️ Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (1.24+)
- kubectl configured
- Container registry access (for images)

### Quick Deploy

```bash
# Create namespace and deploy
kubectl apply -f k8s/deployment.yaml

# Check status
kubectl get pods -n chatppt

# Get service URL
kubectl get svc -n chatppt
```

### Configuration Steps

#### 1. Update Secrets

```bash
# Create secret with your API keys
kubectl create secret generic chatppt-secrets \
  --from-literal=OPENAI_API_KEY=your_key_here \
  --from-literal=AZURE_OPENAI_API_KEY=your_azure_key \
  --from-literal=AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/ \
  --from-literal=AZURE_OPENAI_API_VERSION=2024-02-15-preview \
  -n chatppt
```

#### 2. Update Image Registry

Edit `k8s/deployment.yaml`:
```yaml
spec:
  containers:
  - name: chatppt
    image: ghcr.io/YOUR_USERNAME/chatppt:latest-cpu  # Update this
```

#### 3. Deploy

```bash
kubectl apply -f k8s/deployment.yaml
```

#### 4. Verify Deployment

```bash
# Check pods
kubectl get pods -n chatppt

# Check services
kubectl get svc -n chatppt

# View logs
kubectl logs -f deployment/chatppt-deployment -n chatppt

# Describe pod
kubectl describe pod -n chatppt -l app=chatppt
```

### GPU Deployment

For GPU-enabled deployment:

```bash
# Ensure NVIDIA GPU Operator is installed
kubectl apply -f k8s/deployment-gpu.yaml

# Check GPU allocation
kubectl describe node | grep -A 5 "Allocated resources"
```

### Scaling

```bash
# Manual scaling
kubectl scale deployment chatppt-deployment --replicas=5 -n chatppt

# Auto-scaling is configured via HorizontalPodAutoscaler
kubectl get hpa -n chatppt
```

### Updating Deployment

```bash
# Update image
kubectl set image deployment/chatppt-deployment \
  chatppt=ghcr.io/username/chatppt:v1.1.0 \
  -n chatppt

# Rollback
kubectl rollout undo deployment/chatppt-deployment -n chatppt

# Check rollout status
kubectl rollout status deployment/chatppt-deployment -n chatppt
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions

The project includes a complete CI/CD pipeline (`.github/workflows/ci-cd.yml`) that:

1. **Test** - Runs unit tests on every push/PR
2. **Build** - Builds Docker images for CPU and GPU
3. **Security Scan** - Scans images for vulnerabilities
4. **Deploy Staging** - Auto-deploys to staging on `develop` branch
5. **Deploy Production** - Auto-deploys to production on `main` branch

### Pipeline Configuration

#### Required Secrets

Configure these in GitHub Settings → Secrets:

```
OPENAI_API_KEY           - OpenAI API key
AZURE_OPENAI_API_KEY     - Azure OpenAI key
AZURE_OPENAI_ENDPOINT    - Azure endpoint
DOCKER_USERNAME          - Docker Hub username (if using)
DOCKER_PASSWORD          - Docker Hub password (if using)
KUBECONFIG               - Kubernetes config (for K8s deployment)
```

#### GitHub Container Registry

Images are automatically published to GitHub Container Registry:
- `ghcr.io/username/chatppt:latest-cpu`
- `ghcr.io/username/chatppt:latest-gpu`
- `ghcr.io/username/chatppt:v1.0.0-cpu`

#### Triggering Builds

```bash
# Push to trigger pipeline
git add .
git commit -m "Update feature"
git push origin develop  # Triggers staging deployment

# Merge to main for production
git checkout main
git merge develop
git push origin main  # Triggers production deployment
```

### Custom CI/CD

For other CI/CD platforms (GitLab, Jenkins, etc.), adapt the pipeline:

**Key Steps:**
1. Run tests: `cd src/tests && python run_tests.py`
2. Build image: `docker build -f Dockerfile.cpu -t image:tag .`
3. Push image: `docker push image:tag`
4. Deploy: `kubectl apply -f k8s/deployment.yaml`

---

## ⚙️ Environment Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Yes* | - |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI key | Yes* | - |
| `AZURE_OPENAI_ENDPOINT` | Azure endpoint URL | If using Azure | - |
| `AZURE_OPENAI_API_VERSION` | Azure API version | If using Azure | 2024-02-15-preview |
| `GRADIO_SERVER_NAME` | Server host | No | 0.0.0.0 |
| `GRADIO_SERVER_PORT` | Server port | No | 7860 |
| `LOG_LEVEL` | Logging level | No | INFO |

*Either OpenAI or Azure OpenAI key is required

### Configuration Files

#### `.env` File

```bash
# Copy example
cp .env.example .env

# Edit with your values
nano .env
```

#### `config.json`

Located in project root, configures:
- Input mode
- Prompt paths
- Template paths

---

## 🚀 Production Deployment

### Pre-deployment Checklist

- [ ] Environment variables configured
- [ ] API keys validated
- [ ] Storage volumes configured
- [ ] Resource limits set appropriately
- [ ] Health checks configured
- [ ] Logging configured
- [ ] Monitoring set up
- [ ] Backup strategy in place
- [ ] Security scan passed

### Resource Requirements

#### Minimum (CPU)
- **CPU**: 1 core
- **Memory**: 2GB
- **Storage**: 10GB

#### Recommended (CPU)
- **CPU**: 2 cores
- **Memory**: 4GB
- **Storage**: 50GB

#### GPU Deployment
- **CPU**: 2 cores
- **Memory**: 8GB
- **GPU**: 1x NVIDIA GPU (8GB+ VRAM)
- **Storage**: 100GB

### High Availability Setup

```bash
# Run multiple replicas
kubectl scale deployment chatppt-deployment --replicas=3 -n chatppt

# Ensure pod anti-affinity
# Edit deployment.yaml to add affinity rules
```

### Monitoring

```bash
# Check health
kubectl get pods -n chatppt
curl http://your-service-url/

# View metrics
kubectl top pods -n chatppt

# Application logs
kubectl logs -f deployment/chatppt-deployment -n chatppt
```

### Backup Strategy

```bash
# Backup persistent volumes
kubectl get pvc -n chatppt

# Export configurations
kubectl get all -n chatppt -o yaml > chatppt-backup.yaml
```

---

## 🔒 Security Best Practices

1. **Never commit API keys** - Use secrets management
2. **Use non-root user** - Containers run as non-root
3. **Scan images** - CI/CD includes Trivy scanning
4. **Keep dependencies updated** - Regular updates
5. **Use TLS** - Enable HTTPS in production
6. **Network policies** - Restrict pod communication

---

## 🐛 Troubleshooting

### Common Issues

**Issue: Container fails to start**
```bash
# Check logs
docker logs chatppt

# Common causes:
# - Missing API keys
# - Port already in use
# - Insufficient resources
```

**Issue: GPU not detected**
```bash
# Verify NVIDIA runtime
docker run --rm --gpus all nvidia/cuda:12.1.0-base nvidia-smi

# Check Docker daemon config
cat /etc/docker/daemon.json
```

**Issue: Out of memory**
```bash
# Increase memory limit
docker run -m 4g chatppt:latest-cpu

# For K8s, update resource limits
```

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-container-toolkit)

---

## 📞 Support

For issues and questions:
- Check the main README.md
- Review troubleshooting section
- Check GitHub Issues
- Review application logs

---

**Last Updated**: December 21, 2025  
**Version**: 1.0.0

