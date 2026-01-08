#!/bin/bash

# Script to check if all required dependencies are installed

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Status symbols
CHECK="✓"
CROSS="✗"
WARN="⚠"

# Required Python version
REQUIRED_PYTHON_MAJOR=3
REQUIRED_PYTHON_MINOR=12
REQUIRED_PYTHON_PATCH=12

# Track if all dependencies are met
ALL_DEPS_MET=true

echo ""
echo -e "${BOLD}${BLUE}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${BLUE}║       Setzy Dependency Checker                     ║${NC}"
echo -e "${BOLD}${BLUE}╚════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to compare version numbers
version_ge() {
    [ "$1" = "$2" ] && return 0
    [ "$1" = "$(echo -e "$1\n$2" | sort -V | tail -n1)" ]
}

# Check Docker
echo -e "${CYAN}${BOLD}Checking Docker...${NC}"
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | awk '{print $3}' | sed 's/,//')
    echo -e "  ${GREEN}${CHECK} Docker installed${NC} (version: ${DOCKER_VERSION})"
    
    # Check if Docker is running
    if docker info &> /dev/null; then
        echo -e "  ${GREEN}${CHECK} Docker daemon is running${NC}"
    else
        echo -e "  ${RED}${CROSS} Docker daemon is NOT running${NC}"
        echo -e "  ${YELLOW}→ Please start Docker Desktop or Docker daemon${NC}"
        ALL_DEPS_MET=false
    fi
else
    echo -e "  ${RED}${CROSS} Docker is NOT installed${NC}"
    echo -e "  ${YELLOW}→ Install from: ${NC}https://docs.docker.com/get-docker/"
    ALL_DEPS_MET=false
fi
echo ""

# Check Python
echo -e "${CYAN}${BOLD}Checking Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    PYTHON_PATCH=$(echo $PYTHON_VERSION | cut -d. -f3)
    
    echo -e "  ${GREEN}${CHECK} Python installed${NC} (version: ${PYTHON_VERSION})"
    
    # Check version
    REQUIRED_VERSION="${REQUIRED_PYTHON_MAJOR}.${REQUIRED_PYTHON_MINOR}.${REQUIRED_PYTHON_PATCH}"
    if version_ge "$PYTHON_VERSION" "$REQUIRED_VERSION"; then
        echo -e "  ${GREEN}${CHECK} Python version meets requirement (>= ${REQUIRED_VERSION})${NC}"
    else
        echo -e "  ${RED}${CROSS} Python version ${PYTHON_VERSION} is less than required ${REQUIRED_VERSION}${NC}"
        echo -e "  ${YELLOW}→ Install from: ${NC}https://www.python.org/downloads/"
        ALL_DEPS_MET=false
    fi
else
    echo -e "  ${RED}${CROSS} Python is NOT installed${NC}"
    echo -e "  ${YELLOW}→ Install from: ${NC}https://www.python.org/downloads/"
    ALL_DEPS_MET=false
fi
echo ""

# Check Poetry
echo -e "${CYAN}${BOLD}Checking Poetry...${NC}"
if command -v poetry &> /dev/null; then
    POETRY_VERSION=$(poetry --version | awk '{print $3}' | sed 's/)//')
    echo -e "  ${GREEN}${CHECK} Poetry installed${NC} (version: ${POETRY_VERSION})"
else
    echo -e "  ${RED}${CROSS} Poetry is NOT installed${NC}"
    echo -e "  ${YELLOW}→ Install from: ${NC}https://python-poetry.org/docs/#installation"
    echo -e "  ${YELLOW}→ Quick install: ${NC}curl -sSL https://install.python-poetry.org | python3 -"
    ALL_DEPS_MET=false
fi
echo ""

# Check AWS CLI
echo -e "${CYAN}${BOLD}Checking AWS CLI...${NC}"
if command -v aws &> /dev/null; then
    AWS_VERSION=$(aws --version 2>&1 | awk '{print $1}' | cut -d/ -f2)
    echo -e "  ${GREEN}${CHECK} AWS CLI installed${NC} (version: ${AWS_VERSION})"
    
    # Check AWS credentials
    HAS_CREDENTIALS=false
    if [ -n "$AWS_ACCESS_KEY_ID" ] && [ -n "$AWS_SECRET_ACCESS_KEY" ]; then
        echo -e "  ${GREEN}${CHECK} AWS credentials found in environment variables${NC}"
        HAS_CREDENTIALS=true
    elif [ -f ~/.aws/credentials ]; then
        echo -e "  ${GREEN}${CHECK} AWS credentials file found at ~/.aws/credentials${NC}"
        HAS_CREDENTIALS=true
    fi
    
    if [ "$HAS_CREDENTIALS" = false ]; then
        echo -e "  ${YELLOW}${WARN} No AWS credentials found${NC}"
        echo -e "  ${YELLOW}→ Configure with: ${NC}aws configure"
        echo -e "  ${YELLOW}→ Or set environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY${NC}"
    fi
else
    echo -e "  ${RED}${CROSS} AWS CLI is NOT installed${NC}"
    echo -e "  ${YELLOW}→ Install from: ${NC}https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
    ALL_DEPS_MET=false
fi
echo ""

# Check Docker Compose
echo -e "${CYAN}${BOLD}Checking Docker Compose...${NC}"
if command -v docker &> /dev/null && docker compose version &> /dev/null; then
    COMPOSE_VERSION=$(docker compose version | awk '{print $4}' | sed 's/v//')
    echo -e "  ${GREEN}${CHECK} Docker Compose installed${NC} (version: ${COMPOSE_VERSION})"
elif command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version | awk '{print $4}' | sed 's/,//')
    echo -e "  ${GREEN}${CHECK} Docker Compose installed${NC} (version: ${COMPOSE_VERSION})"
else
    echo -e "  ${RED}${CROSS} Docker Compose is NOT installed${NC}"
    echo -e "  ${YELLOW}→ Included with Docker Desktop or install from: ${NC}https://docs.docker.com/compose/install/"
    ALL_DEPS_MET=false
fi
echo ""

# Check Node.js
echo -e "${CYAN}${BOLD}Checking Node.js...${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version | sed 's/v//')
    echo -e "  ${GREEN}${CHECK} Node.js installed${NC} (version: ${NODE_VERSION})"
    
    # Check npm
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        echo -e "  ${GREEN}${CHECK} npm installed${NC} (version: ${NPM_VERSION})"
    else
        echo -e "  ${YELLOW}${WARN} npm is NOT installed${NC}"
        ALL_DEPS_MET=false
    fi
else
    echo -e "  ${RED}${CROSS} Node.js is NOT installed${NC}"
    echo -e "  ${YELLOW}→ Install from: ${NC}https://nodejs.org/"
    ALL_DEPS_MET=false
fi
echo ""

# Check Git
echo -e "${CYAN}${BOLD}Checking Git...${NC}"
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version | awk '{print $3}')
    echo -e "  ${GREEN}${CHECK} Git installed${NC} (version: ${GIT_VERSION})"
else
    echo -e "  ${RED}${CROSS} Git is NOT installed${NC}"
    echo -e "  ${YELLOW}→ Install from: ${NC}https://git-scm.com/downloads"
    ALL_DEPS_MET=false
fi
echo ""

# Check pyenv (optional)
echo -e "${CYAN}${BOLD}Checking pyenv (optional)...${NC}"
if command -v pyenv &> /dev/null; then
    PYENV_VERSION=$(pyenv --version | awk '{print $2}')
    echo -e "  ${GREEN}${CHECK} pyenv installed${NC} (version: ${PYENV_VERSION})"
else
    echo -e "  ${YELLOW}${WARN} pyenv is NOT installed (optional)${NC}"
    echo -e "  ${YELLOW}→ pyenv helps manage multiple Python versions${NC}"
    echo -e "  ${YELLOW}→ Install from: ${NC}https://github.com/pyenv/pyenv#installation"
fi
echo ""

# Final summary
echo -e "${BOLD}${BLUE}════════════════════════════════════════════════════${NC}"
if [ "$ALL_DEPS_MET" = true ]; then
    echo -e "${GREEN}${BOLD}${CHECK} All required dependencies are installed!${NC}"
    echo -e "${GREEN}You're ready to start working on Setzy! 🚀${NC}"
else
    echo -e "${RED}${BOLD}${CROSS} Some required dependencies are missing or not running.${NC}"
    echo -e "${YELLOW}Please install the missing dependencies listed above.${NC}"
fi
echo -e "${BOLD}${BLUE}════════════════════════════════════════════════════${NC}"
echo ""

# Exit with appropriate code
if [ "$ALL_DEPS_MET" = true ]; then
    exit 0
else
    exit 1
fi
