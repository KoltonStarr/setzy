#!/bin/bash

# Script to build Docker images for different components of the Setzy project

set -e  # Exit on error

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    echo "Usage: $0 {agent|data_pipeline|frontend|uploader}"
    echo ""
    echo "Options:"
    echo "  agent          Build the agent service"
    echo "  data_pipeline  Build the data pipeline service"
    echo "  frontend       Build the frontend service"
    echo "  uploader       Build the uploader service"
    exit 1
}

# Check if component argument is provided
if [ $# -eq 0 ]; then
    echo -e "${RED}Error: No component specified${NC}"
    usage
fi

COMPONENT=$1

# Build based on component
case "$COMPONENT" in
    agent)
        echo -e "${BLUE}Building agent service...${NC}"
        docker build -t setzy-agent:latest -f ./setzy_agent/Dockerfile .
        echo -e "${GREEN}✓ Agent service built successfully${NC}"
        ;;
    
    embedding_pipeline)
        echo -e "${BLUE}Building embedding pipeline service...${NC}"
        docker build -t embedding-pipeline -f embedding_pipeline/src/Dockerfile .
        echo -e "${GREEN}✓ Embedding pipeline service built successfully${NC}"
        ;;
    
    frontend)
        echo -e "${BLUE}Building frontend service...${NC}"
        # TODO: Implement frontend build
        echo -e "${RED}Frontend build not yet implemented${NC}"
        exit 1
        ;;
    
    uploader)
        echo -e "${BLUE}Building uploader service...${NC}"
        docker build -t setzy-uploader -f uploader/Dockerfile .
        echo -e "${GREEN}✓ Uploader service built successfully${NC}"
        ;;
    
    *)
        echo -e "${RED}Error: Unknown component '$COMPONENT'${NC}"
        usage
        ;;
esac
