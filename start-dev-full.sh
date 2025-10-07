#!/bin/bash

# =============================================================================
# Betting League Championship - Development Environment Startup Script
# =============================================================================
# This script starts the complete development environment:
# - Backend services (FastAPI, PostgreSQL, Keycloak, Adminer)
# - Frontend development server (Angular)
# =============================================================================

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
DOCKER_COMPOSE_FILE="docker-compose.dev.yml"
FRONTEND_DIR="frontend/betting-league-app"
BACKEND_WAIT_TIME=30
FRONTEND_WAIT_TIME=10

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

# Function to check if Docker is running
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed or not in PATH"
        exit 1
    fi

    if ! docker info &> /dev/null; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi

    print_success "Docker is running"
}

# Function to check if Node.js and nvm are available
check_node() {
    # Set up nvm
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

    if ! command -v nvm &> /dev/null; then
        print_error "nvm is not installed. Please install nvm first."
        exit 1
    fi

    # Use Node.js v22.20.0
    print_status "Setting up Node.js v22.20.0..."
    nvm use 22.20.0 || {
        print_error "Failed to switch to Node.js v22.20.0. Please install it with: nvm install 22.20.0"
        exit 1
    }

    print_success "Node.js $(node --version) and npm $(npm --version) are ready"
}

# Function to stop existing services
stop_services() {
    print_status "Stopping any existing services..."
    
    # Stop Docker services
    if [ -f "$DOCKER_COMPOSE_FILE" ]; then
        docker compose -f "$DOCKER_COMPOSE_FILE" down --remove-orphans &> /dev/null || true
    fi
    
    # Kill any existing Angular dev servers
    pkill -f "ng serve" &> /dev/null || true
    pkill -f "@angular/cli.*serve" &> /dev/null || true
    
    print_success "Stopped existing services"
}

# Function to start backend services
start_backend() {
    print_header "STARTING BACKEND SERVICES"
    
    if [ ! -f "$DOCKER_COMPOSE_FILE" ]; then
        print_error "Docker Compose file not found: $DOCKER_COMPOSE_FILE"
        exit 1
    fi

    print_status "Starting backend services (PostgreSQL, Keycloak, FastAPI, Adminer)..."
    
    # Start services in detached mode
    docker compose -f "$DOCKER_COMPOSE_FILE" up -d
    
    print_status "Waiting for services to be healthy (this may take up to ${BACKEND_WAIT_TIME}s)..."
    
    # Wait for services to be healthy
    local max_attempts=$((BACKEND_WAIT_TIME / 2))
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        sleep 2
        
        # Check service health
        local postgres_health=$(docker compose -f "$DOCKER_COMPOSE_FILE" ps postgres --format "table {{.Health}}" | tail -n +2)
        local backend_health=$(docker compose -f "$DOCKER_COMPOSE_FILE" ps backend --format "table {{.Health}}" | tail -n +2)
        
        if [[ "$postgres_health" == *"healthy"* ]] && [[ "$backend_health" == *"healthy"* ]]; then
            print_success "Backend services are healthy!"
            break
        fi
        
        if [ $attempt -eq $max_attempts ]; then
            print_warning "Services may still be starting up. Continuing anyway..."
            print_status "You can check service status with: docker compose -f $DOCKER_COMPOSE_FILE ps"
            break
        fi
        
        echo -n "."
        ((attempt++))
    done
    
    echo ""
    
    # Display service status
    print_status "Current service status:"
    docker compose -f "$DOCKER_COMPOSE_FILE" ps
    
    echo ""
    print_success "Backend services started!"
    print_status "🐘 PostgreSQL: http://localhost:5432"
    print_status "🔐 Keycloak: http://localhost:8080"
    print_status "🚀 FastAPI: http://localhost:8000"
    print_status "💾 Adminer: http://localhost:8081"
}

# Function to start frontend
start_frontend() {
    print_header "STARTING FRONTEND DEVELOPMENT SERVER"
    
    if [ ! -d "$FRONTEND_DIR" ]; then
        print_error "Frontend directory not found: $FRONTEND_DIR"
        exit 1
    fi
    
    cd "$FRONTEND_DIR"
    
    print_status "Installing/updating frontend dependencies..."
    npm install --silent
    
    print_status "Starting Angular development server..."
    print_status "Frontend will be available at: http://localhost:4200"
    
    # Start Angular dev server in the background
    npx @angular/cli@latest serve &
    FRONTEND_PID=$!
    
    # Wait a moment for the server to start
    sleep $FRONTEND_WAIT_TIME
    
    # Check if the process is still running
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        print_success "Frontend development server started (PID: $FRONTEND_PID)"
    else
        print_error "Failed to start frontend development server"
        exit 1
    fi
    
    # Return to root directory
    cd - > /dev/null
}

# Function to display final status
show_final_status() {
    print_header "DEVELOPMENT ENVIRONMENT READY"
    
    echo -e "${GREEN}🎉 All services are running!${NC}"
    echo ""
    echo -e "${CYAN}📱 Frontend (Angular):${NC} http://localhost:4200"
    echo -e "${CYAN}🚀 Backend API (FastAPI):${NC} http://localhost:8000"
    echo -e "${CYAN}📊 API Documentation:${NC} http://localhost:8000/docs"
    echo -e "${CYAN}🔐 Keycloak Admin:${NC} http://localhost:8080"
    echo -e "${CYAN}💾 Database Admin (Adminer):${NC} http://localhost:8081"
    echo ""
    echo -e "${YELLOW}📝 Useful Commands:${NC}"
    echo "  • View backend logs: docker compose -f $DOCKER_COMPOSE_FILE logs -f"
    echo "  • Stop all services: ./scripts/stop-dev.sh (or Ctrl+C)"
    echo "  • Restart backend: docker compose -f $DOCKER_COMPOSE_FILE restart"
    echo "  • Frontend logs: Check this terminal output"
    echo ""
    echo -e "${PURPLE}🔧 Development Tips:${NC}"
    echo "  • Backend API auto-reloads on code changes"
    echo "  • Frontend auto-reloads on code changes"
    echo "  • Database data persists between restarts"
    echo "  • Use Adminer for database management"
    echo ""
}

# Function to handle cleanup on exit
cleanup() {
    print_status "Shutting down development environment..."
    
    # Kill frontend process if it exists
    if [ ! -z "$FRONTEND_PID" ] && kill -0 $FRONTEND_PID 2>/dev/null; then
        print_status "Stopping frontend development server..."
        kill $FRONTEND_PID
    fi
    
    # Stop Docker services
    print_status "Stopping backend services..."
    docker compose -f "$DOCKER_COMPOSE_FILE" down
    
    print_success "Development environment stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Main execution
main() {
    print_header "BETTING LEAGUE CHAMPIONSHIP - DEV SETUP"
    
    print_status "🏁 Starting development environment..."
    echo ""
    
    # Run checks
    check_docker
    check_node
    
    # Stop any existing services
    stop_services
    
    # Start services
    start_backend
    start_frontend
    
    # Show final status
    show_final_status
    
    # Keep script running and wait for user interrupt
    print_status "Press Ctrl+C to stop all services"
    print_status "Monitoring services... (logs will appear below)"
    echo ""
    
    # Follow logs from both frontend and backend
    tail -f /dev/null & wait
}

# Run main function
main "$@"