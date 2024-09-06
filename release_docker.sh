#!/bin/bash

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to extract the latest release version from git branches
get_latest_release_version() {
    git fetch --all >/dev/null 2>&1
    latest_release=$(git branch -r | grep 'origin/release/' | sed 's/.*\/release\///' | sort -V | tail -n 1)
    echo "$latest_release"
}

# Get the latest release version
VERSION=$(get_latest_release_version | tr -d '\n')

if [ -z "$VERSION" ]; then
    echo -e "${RED}Error: No release branch found.${NC}"
    exit 1
fi

# Set the Docker image name and tags
IMAGE_NAME="dontic/postifyai"
VERSION_TAG="${IMAGE_NAME}:${VERSION}"
LATEST_TAG="${IMAGE_NAME}:latest"

# Build the Docker image
echo -e "${BLUE}Building Docker image: ${YELLOW}$VERSION_TAG${NC}"
docker build -t "$VERSION_TAG" -t "$LATEST_TAG" .

# Check if the build was successful
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Docker build failed.${NC}"
    exit 1
fi

# Push the Docker image with version tag
echo -e "${BLUE}Pushing Docker image: ${YELLOW}$VERSION_TAG${NC}"
docker push "$VERSION_TAG"

# Check if the push was successful
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Docker push failed for $VERSION_TAG.${NC}"
    exit 1
fi

# Push the Docker image with latest tag
echo -e "${BLUE}Pushing Docker image: ${YELLOW}$LATEST_TAG${NC}"
docker push "$LATEST_TAG"

# Check if the push was successful
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Docker push failed for $LATEST_TAG.${NC}"
    exit 1
fi

echo -e "${GREEN}Successfully built and pushed Docker images:${NC}"
echo -e "  - ${YELLOW}$VERSION_TAG${NC}"
echo -e "  - ${YELLOW}$LATEST_TAG${NC}"
