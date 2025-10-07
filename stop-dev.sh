#!/bin/bash

# =============================================================================
# Betting League Championship - Stop Development Environment Script
# =============================================================================
# This script stops all development services:
# - Frontend development server (Angular)
# - Backend services (FastAPI, PostgreSQL, Keycloak, Adminer)
# =============================================================================

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
DOCKER_COMPOSE_FILE="docker-compose.dev.yml"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${PURPLE}================================${NC}"
    echo -e "${PURPLE}$1${NC}"
    echo -e "${PURPLE}================================${NC}"
}

main() {
    print_header "STOPPING DEV ENVIRONMENT"
    
    # Stop Angular development servers
    print_status "Stopping frontend development servers..."
    pkill -f "ng serve" &> /dev/null || true
    pkill -f "@angular/cli.*serve" &> /dev/null || true
    pkill -f "npx @angular/cli" &> /dev/null || true
    print_success "Frontend servers stopped"
    
    # Stop Docker services
    if [ -f "$DOCKER_COMPOSE_FILE" ]; then
        print_status "Stopping backend services..."
        docker compose -f "$DOCKER_COMPOSE_FILE" down --remove-orphans
        print_success "Backend services stopped"
    else
        print_warning "Docker Compose file not found: $DOCKER_COMPOSE_FILE"
    fi
    
    # Optional: Clean up Docker resources
    read -p "Do you want to clean up Docker volumes and networks? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Cleaning up Docker resources..."
        docker compose -f "$DOCKER_COMPOSE_FILE" down -v --remove-orphans 2>/dev/null || true
        docker system prune -f 2>/dev/null || true
        print_success "Docker resources cleaned up"
    fi
    
    print_success "🎉 Development environment stopped successfully"
}

main "$@"