#!/bin/bash

# Build script for Docker images

set -e

IMAGE_NAME="cold-email-frontend"
VERSION=${1:-latest}

echo "Building Docker images for $IMAGE_NAME:$VERSION"

# Build production image
echo "Building production image..."
docker build --target production -t $IMAGE_NAME:$VERSION .

# Build development image
echo "Building development image..."
docker build --target development -t $IMAGE_NAME:dev .

echo "Build completed successfully!"
echo ""
echo "Available images:"
echo "  Production: $IMAGE_NAME:$VERSION"
echo "  Development: $IMAGE_NAME:dev"
echo ""
echo "To run production:"
echo "  docker run -p 80:80 $IMAGE_NAME:$VERSION"
echo ""
echo "To run development:"
echo "  docker run -p 3000:3000 $IMAGE_NAME:dev" 