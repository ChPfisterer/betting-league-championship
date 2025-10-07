#!/bin/bash

# =============================================================================
# Betting League Championship - Frontend Only Development Script
# =============================================================================
# This script starts only the Angular frontend development server
# Prerequisites: Backend services should be running (use ./start-backend.sh)
# =============================================================================

set -e  # Exit on any error

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_header() {
    echo -e "${PURPLE}$1${NC}"
}

# Print header
echo ""
print_header "================================"
print_header "FRONTEND DEVELOPMENT SERVER"
print_header "================================"

# Check if backend is running
print_status "Checking if backend services are running..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    print_success "Backend is running at http://localhost:8000"
else
    print_warning "Backend doesn't seem to be running at http://localhost:8000"
    print_warning "Start backend services first: ./start-backend.sh"
    echo ""
fi

# Navigate to frontend directory
FRONTEND_DIR="frontend/betting-league-app"
if [ ! -d "$FRONTEND_DIR" ]; then
    echo -e "${RED}[ERROR]${NC} Frontend directory not found: $FRONTEND_DIR"
    exit 1
fi

print_status "Navigating to frontend directory: $FRONTEND_DIR"
cd "$FRONTEND_DIR"

# Setup Node.js environment
print_status "Setting up Node.js environment..."

# Ensure we're using the correct Node.js version
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

# Use Node.js v22.12.0 (minimum required for Angular 20)
if command -v nvm &> /dev/null; then
    print_status "Using nvm to set Node.js version..."
    nvm use 22.12.0 || nvm install 22.12.0
else
    print_warning "nvm not found, using system Node.js"
fi

# Verify versions and compatibility
NODE_VERSION=$(node --version)
print_status "Node.js version: $NODE_VERSION"
print_status "npm version: $(npm --version)"

# Check if Node version meets Angular 20 requirements
NODE_MAJOR=$(echo $NODE_VERSION | sed 's/v\([0-9]*\).*/\1/')
if [ "$NODE_MAJOR" -lt 20 ]; then
    echo -e "\033[0;31m[ERROR]\033[0m Node.js version $NODE_VERSION is too old for Angular 20"
    echo -e "\033[0;31m[ERROR]\033[0m Please install Node.js v20.19+ or v22.12+"
    exit 1
fi

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    print_status "Installing dependencies..."
    npm install
fi

# Start the Angular development server
print_header "================================"
print_header "STARTING ANGULAR DEV SERVER"
print_header "================================"
print_success "Frontend will be available at: http://localhost:4200"
print_status "Press Ctrl+C to stop the server"
echo ""

# Start Angular development server with error handling
print_status "Starting Angular development server..."
if ! npx @angular/cli@latest serve; then
    echo -e "\033[0;31m[ERROR]\033[0m Failed to start Angular development server"
    echo -e "\033[0;31m[ERROR]\033[0m This might be due to:"
    echo -e "\033[0;31m[ERROR]\033[0m   - Incompatible Node.js version"
    echo -e "\033[0;31m[ERROR]\033[0m   - Missing dependencies (try: npm install)"
    echo -e "\033[0;31m[ERROR]\033[0m   - Port 4200 already in use"
    exit 1
fi