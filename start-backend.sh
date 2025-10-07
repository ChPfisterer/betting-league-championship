#!/bin/bash

# =============================================================================
# Betting League Championship - Backend Only Development Script
# =============================================================================
# This script starts only the backend services:
# - Backend services (FastAPI, PostgreSQL, Keycloak, Adminer)
# Use this when you want to run the frontend separately
# =============================================================================

set -e  # Exit on any error

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
DOCKER_COMPOSE_FILE="docker-compose.dev.yml"

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_header() {
    echo -e "${PURPLE}================================${NC}"
    echo -e "${PURPLE}$1${NC}"
    echo -e "${PURPLE}================================${NC}"
}

main() {
    print_header "BACKEND SERVICES ONLY"
    
    print_status "Starting backend services..."
    docker compose -f "$DOCKER_COMPOSE_FILE" up -d
    
    print_status "Waiting for services to be ready..."
    sleep 10
    
    print_status "Service status:"
    docker compose -f "$DOCKER_COMPOSE_FILE" ps
    
    print_header "BACKEND READY"
    echo -e "${GREEN}🚀 Backend services are running!${NC}"
    echo ""
    echo "🚀 FastAPI: http://localhost:8000"
    echo "📊 API Docs: http://localhost:8000/docs"
    echo "🔐 Keycloak: http://localhost:8080"
    echo "💾 Adminer: http://localhost:8081"
    echo "🐘 PostgreSQL: localhost:5432"
    echo ""
    echo -e "${BLUE}📋 Database is automatically seeded with:${NC}"
    echo "  - FIFA World Cup 2022 data (historical)"
    echo "  - Real Bundesliga 2025/26 data (current season)"
    echo ""
    echo "To manually re-seed data:"
    echo "  ./seed-data.sh"
    echo ""
    echo "To start frontend separately:"
    echo "  cd frontend/betting-league-app && ./start-dev.sh"
    echo ""
    echo "To stop services:"
    echo "  ./stop-dev.sh"
}

main "$@"