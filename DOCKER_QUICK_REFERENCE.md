# 🚀 ChatPPT Docker & CI/CD Quick Reference

## ⚡ Quick Commands

### Docker

```bash
# Build
docker build -f Dockerfile.cpu -t chatppt:latest-cpu .

# Run
docker run -p 7860:7860 -e OPENAI_API_KEY=key chatppt:latest-cpu

# With volumes
docker run -p 7860:7860 \
  -v $(pwd)/output:/app/output \
  -e OPENAI_API_KEY=key \
  chatppt:latest-cpu
```

### Docker Compose

```bash
# Setup
cp .env.example .env && nano .env

# Start
docker-compose up -d

# Logs
docker-compose logs -f

# Stop
docker-compose down
```

### Kubernetes

```bash
# Deploy
kubectl apply -f k8s/deployment.yaml

# Status
kubectl get all -n chatppt

# Logs
kubectl logs -f deployment/chatppt-deployment -n chatppt

# Scale
kubectl scale deployment chatppt-deployment --replicas=5 -n chatppt
```

### Build Scripts

```bash
# Linux/Mac
./build-docker.sh --type cpu
./build-docker.sh --type gpu
./build-docker.sh --type all --version 1.0.0

# Windows
build-docker.bat --type cpu
```

## 📁 File Overview

```
├── Dockerfile.cpu           - CPU build
├── Dockerfile.gpu           - GPU build
├── docker-compose.yml       - Compose config
├── .dockerignore            - Build exclusions
├── .env.example             - Config template
├── build-docker.sh/bat      - Build scripts
├── .github/workflows/       - CI/CD pipeline
└── k8s/                     - K8s configs
```

## 🔑 Environment Variables

```bash
OPENAI_API_KEY=your_key
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SERVER_PORT=7860
```

## 📊 Resource Requirements

| Deployment | CPU | Memory | Storage |
|------------|-----|--------|---------|
| Minimum    | 1   | 2GB    | 10GB    |
| Recommended| 2   | 4GB    | 50GB    |
| GPU        | 2   | 8GB    | 100GB   |

## 🎯 Access Points

- **Local**: http://localhost:7860
- **Docker**: http://localhost:7860
- **K8s**: Get from `kubectl get svc -n chatppt`

## 🐛 Troubleshooting

```bash
# Check logs
docker logs chatppt
kubectl logs -f deployment/chatppt-deployment -n chatppt

# Check health
curl http://localhost:7860/

# Restart
docker restart chatppt
kubectl rollout restart deployment/chatppt-deployment -n chatppt
```

## 📚 Documentation

- **Full Guide**: `docs/DOCKER_DEPLOYMENT.md`
- **Summary**: `DOCKER_CICD_SUMMARY.md`
- **Unit Tests**: `src/tests/README.md`

## ✅ Checklist

Before deployment:
- [ ] Copy .env.example to .env
- [ ] Set API keys
- [ ] Choose deployment method
- [ ] Review resource limits
- [ ] Configure volumes
- [ ] Test locally
- [ ] Deploy to staging
- [ ] Deploy to production

---
**Version**: 1.0.0 | **Updated**: Dec 21, 2025

