#!/bin/bash

# =============================================================================
# Betting League Championship - Data Seeding Script
# =============================================================================
# This script seeds the database with all competition data
# Can be run independently or as part of environment startup
# =============================================================================

set -e

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
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

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

main() {
    print_header "DATABASE SEEDING"
    
    # Check if we're in the backend directory
    if [[ ! -f "complete_data_seeder.py" ]]; then
        print_status "Navigating to backend directory..."
        cd backend
    fi
    
    # Check if database is accessible
    print_status "Checking database connection..."
    if ! python3 -c "import psycopg2; psycopg2.connect(host='localhost', port=5432, database='betting_championship', user='postgres', password='postgres123')" 2>/dev/null; then
        print_error "Database not accessible. Please ensure PostgreSQL is running."
        echo "You may need to start the backend services first:"
        echo "  ./start-backend.sh"
        exit 1
    fi
    
    print_success "Database connection confirmed"
    
    # Run the comprehensive data seeder
    print_status "Running comprehensive data seeding..."
    python3 complete_data_seeder.py
    
    print_header "SEEDING COMPLETE"
    print_success "Database has been seeded with competition data!"
    echo ""
    echo "📊 Available data:"
    echo "  - FIFA World Cup 2022 (historical)"
    echo "  - Bundesliga 2025/26 (current season)"
    echo ""
    echo "🚀 You can now test the betting functionality!"
}

main "$@"