#!/bin/bash
# Build script for ChatPPT Docker images

set -e

echo "======================================"
echo "ChatPPT Docker Build Script"
echo "======================================"

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -t, --type TYPE      Build type: cpu, gpu, or all (default: cpu)"
    echo "  -v, --version VER    Version tag (default: latest)"
    echo "  -r, --registry REG   Registry URL (default: none)"
    echo "  -p, --push           Push to registry after build"
    echo "  -h, --help           Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --type cpu"
    echo "  $0 --type all --version 1.0.0"
    echo "  $0 --type cpu --registry ghcr.io/myuser/chatppt --push"
    exit 1
}

# Default values
BUILD_TYPE="cpu"
VERSION="latest"
REGISTRY=""
PUSH=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--type)
            BUILD_TYPE="$2"
            shift 2
            ;;
        -v|--version)
            VERSION="$2"
            shift 2
            ;;
        -r|--registry)
            REGISTRY="$2"
            shift 2
            ;;
        -p|--push)
            PUSH=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

# Validate build type
if [[ ! "$BUILD_TYPE" =~ ^(cpu|gpu|all)$ ]]; then
    echo "Error: Invalid build type. Must be cpu, gpu, or all"
    exit 1
fi

# Set image name
if [ -n "$REGISTRY" ]; then
    IMAGE_NAME="$REGISTRY"
else
    IMAGE_NAME="chatppt"
fi

# Function to build an image
build_image() {
    local variant=$1
    local dockerfile="Dockerfile.$variant"
    local tag="${IMAGE_NAME}:${VERSION}-${variant}"

    echo ""
    echo "Building $variant image: $tag"
    echo "--------------------------------------"

    if [ ! -f "$dockerfile" ]; then
        echo "Error: Dockerfile not found: $dockerfile"
        return 1
    fi

    docker build \
        -f "$dockerfile" \
        -t "$tag" \
        --build-arg VERSION="$VERSION" \
        .

    # Also tag as latest for this variant
    docker tag "$tag" "${IMAGE_NAME}:latest-${variant}"

    echo "✅ Successfully built: $tag"

    # Push if requested
    if [ "$PUSH" = true ]; then
        echo "Pushing $tag to registry..."
        docker push "$tag"
        docker push "${IMAGE_NAME}:latest-${variant}"
        echo "✅ Successfully pushed: $tag"
    fi
}

# Build images based on type
echo ""
echo "Build Configuration:"
echo "  Type: $BUILD_TYPE"
echo "  Version: $VERSION"
echo "  Image: $IMAGE_NAME"
echo "  Push: $PUSH"
echo ""

if [ "$BUILD_TYPE" = "all" ]; then
    build_image "cpu"
    build_image "gpu"
else
    build_image "$BUILD_TYPE"
fi

echo ""
echo "======================================"
echo "Build completed successfully!"
echo "======================================"
echo ""
echo "Available images:"
docker images | grep chatppt | head -n 10

echo ""
echo "To run the container:"
if [ "$BUILD_TYPE" = "gpu" ] || [ "$BUILD_TYPE" = "all" ]; then
    echo "  docker run -p 7860:7860 --gpus all ${IMAGE_NAME}:latest-gpu"
fi
if [ "$BUILD_TYPE" = "cpu" ] || [ "$BUILD_TYPE" = "all" ]; then
    echo "  docker run -p 7860:7860 ${IMAGE_NAME}:latest-cpu"
fi
echo ""
echo "Or use docker-compose:"
echo "  docker-compose up -d"

