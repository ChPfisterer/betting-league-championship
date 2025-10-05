#!/bin/bash
# Professional Development Environment Deployment Script
# This script sets up a complete development environment with database, tables, and seed data

set -e  # Exit on any error

echo "🚀 BETTING LEAGUE CHAMPIONSHIP - DEV ENVIRONMENT DEPLOYMENT"
echo "============================================================"

# Configuration
PROJECT_NAME="betting-league-championship"
COMPOSE_FILE="docker-compose.dev.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    log_info "Checking Docker status..."
    if ! docker info > /dev/null 2>&1; then
        log_error "Docker is not running. Please start Docker Desktop and try again."
        exit 1
    fi
    log_success "Docker is running"
}

# Function to clean up existing environment
cleanup_environment() {
    log_info "Cleaning up existing environment..."
    
    # Stop and remove containers and volumes
    docker compose -f $COMPOSE_FILE down -v --remove-orphans 2>/dev/null || true
    
    # Remove any dangling images and volumes
    docker system prune -f > /dev/null 2>&1 || true
    
    log_success "Environment cleaned up"
}

# Function to build and start services
start_services() {
    log_info "Building and starting services..."
    
    # Build and start all services
    docker compose -f $COMPOSE_FILE up --build -d
    
    log_success "Services started"
}

# Function to wait for services to be healthy
wait_for_services() {
    log_info "Waiting for services to be healthy..."
    
    # Wait for PostgreSQL
    log_info "Waiting for PostgreSQL to be ready..."
    timeout=60
    while [ $timeout -gt 0 ]; do
        if docker compose -f $COMPOSE_FILE exec -T postgres pg_isready -U postgres > /dev/null 2>&1; then
            log_success "PostgreSQL is ready"
            break
        fi
        sleep 2
        timeout=$((timeout - 2))
    done
    
    if [ $timeout -le 0 ]; then
        log_error "PostgreSQL failed to start within 60 seconds"
        exit 1
    fi
    
    # Wait for Backend
    log_info "Waiting for Backend API to be ready..."
    timeout=60
    while [ $timeout -gt 0 ]; do
        if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
            log_success "Backend API is ready"
            break
        fi
        sleep 2
        timeout=$((timeout - 2))
    done
    
    if [ $timeout -le 0 ]; then
        log_error "Backend API failed to start within 60 seconds"
        exit 1
    fi
}

# Function to create database tables
# Function to create database tables and add comprehensive seed data
create_tables_and_seed() {
    log_info "Creating database tables and adding comprehensive FIFA World Cup 2022 seed data..."
    
    # First create all database tables
    log_info "Creating database tables..."
    docker compose -f $COMPOSE_FILE exec backend python -c "
import sys; sys.path.append('/app/src')
from database import Base, engine

# Import ALL models to register them with Base
from models.sport import Sport
from models.season import Season  
from models.team import Team
from models.player import Player
from models.competition import Competition
from models.match import Match
from models.result import Result
from models.user import User
from models.group import Group
from models.group_membership import GroupMembership
from models.bet import Bet
from models.audit_log import AuditLog

print('Creating database tables...')
Base.metadata.create_all(bind=engine)
print('Database tables created successfully!')
"
    
    if [ $? -ne 0 ]; then
        log_error "Failed to create database tables"
        return 1
    fi
    
    # Use the COMPLETE FIFA World Cup 2022 seeder
    log_info "Running COMPLETE FIFA World Cup 2022 seeder (100+ players, 64 matches)..."
    # Use the FINAL comprehensive seeder as primary option
    docker compose -f $COMPOSE_FILE exec backend python /app/FINAL_complete_world_cup_seeder.py    if [ $? -eq 0 ]; then
        log_success "Database tables and COMPREHENSIVE FIFA World Cup 2022 dataset created successfully"
        
        # Display comprehensive summary
        log_info "Displaying comprehensive seed data summary..."
        docker compose -f $COMPOSE_FILE exec -T postgres psql -U postgres -d betting_championship << 'EOF'
-- Comprehensive data summary
SELECT 
    'sports' as table_name, 
    count(*) as records,
    string_agg(name, ', ') as sample_data
FROM sports
UNION ALL
SELECT 
    'teams', 
    count(*),
    CASE 
        WHEN count(*) <= 5 THEN string_agg(name, ', ' ORDER BY name)
        ELSE (SELECT string_agg(name, ', ' ORDER BY name) FROM (SELECT name FROM teams ORDER BY name LIMIT 5) t) || ' (+' || (count(*) - 5)::text || ' more)'
    END
FROM teams  
UNION ALL
SELECT 
    'users', 
    count(*),
    string_agg(username, ', ')
FROM users
UNION ALL
SELECT 
    'seasons', 
    count(*),
    string_agg(name, ', ')
FROM seasons
UNION ALL
SELECT 
    'competitions', 
    count(*),
    string_agg(name, ', ')
FROM competitions
UNION ALL
SELECT 
    'matches', 
    count(*),
    CASE WHEN count(*) > 0 THEN count(*)::text || ' matches loaded' ELSE 'No matches' END
FROM matches
UNION ALL
SELECT 
    'players', 
    count(*),
    CASE WHEN count(*) > 0 THEN count(*)::text || ' players loaded' ELSE 'No players' END
FROM players
ORDER BY table_name;

\echo ''
\echo 'Sample Teams:'
SELECT name, country FROM teams ORDER BY name LIMIT 10;

\echo ''
\echo 'Competition Details:'
SELECT name, format_type, status, start_date, end_date FROM competitions;
EOF
        
    else
        log_error "Failed to create tables and add comprehensive seed data"
        log_info "Falling back to basic SQL approach..."
        
        # Fallback: Create tables manually then add basic data
        log_info "Creating database tables manually..."
        docker compose -f $COMPOSE_FILE exec backend python -c "
import sys; sys.path.append('/app/src')
from models import *
from database import Base, engine
Base.metadata.create_all(bind=engine)
"
        
        # Add basic fallback seed data
        docker compose -f $COMPOSE_FILE exec -T postgres psql -U postgres -d betting_championship << 'EOF'
-- Basic fallback seed data
INSERT INTO sports (id, name, slug, description, category, is_active, popularity_score, rules, created_at, updated_at)
VALUES (gen_random_uuid(), 'Football', 'football', 'Association Football (Soccer)', 'team_sport', true, 95, '{"players_per_team": 11, "match_duration": 90}', NOW(), NOW())
ON CONFLICT (slug) DO NOTHING;

WITH sport_id AS (SELECT id FROM sports WHERE slug = 'football' LIMIT 1)
INSERT INTO seasons (id, name, slug, sport_id, year, start_date, end_date, is_current, status, prize_pool_total, created_at, updated_at)
VALUES (gen_random_uuid(), '2022 FIFA World Cup', 'fifa-world-cup-2022', (SELECT id FROM sport_id), 2022, '2022-11-20', '2022-12-18', false, 'completed', 440000000.00, NOW(), NOW())
ON CONFLICT (slug) DO NOTHING;

WITH sport_id AS (SELECT id FROM sports WHERE slug = 'football' LIMIT 1)
INSERT INTO teams (id, name, slug, short_name, sport_id, country, city, founded_year, is_active, max_players, created_at, updated_at)
SELECT gen_random_uuid(), 'Argentina', 'argentina', 'ARG', sport_id.id, 'Argentina', 'Buenos Aires', 1901, true, 25, NOW(), NOW()
FROM sport_id WHERE NOT EXISTS (SELECT 1 FROM teams WHERE slug = 'argentina')
UNION ALL
SELECT gen_random_uuid(), 'France', 'france', 'FRA', sport_id.id, 'France', 'Paris', 1904, true, 25, NOW(), NOW()
FROM sport_id WHERE NOT EXISTS (SELECT 1 FROM teams WHERE slug = 'france');

SELECT 'Basic fallback seed data added' as status;
EOF
        
        if [ $? -eq 0 ]; then
            log_success "Basic seed data added as fallback"
        else
            log_error "Failed to add even basic seed data"
            return 1
        fi
    fi
}

# Function to add comprehensive FIFA World Cup 2022 seed data
add_seed_data() {
    log_info "Adding comprehensive FIFA World Cup 2022 seed data..."
    
    # Use the FINAL comprehensive Python seeder for complete dataset
    log_info "Running FINAL comprehensive seed data script with complete FIFA World Cup 2022 dataset..."
    docker compose -f $COMPOSE_FILE exec backend python /app/FINAL_complete_world_cup_seeder.py
    
    if [ $? -eq 0 ]; then
        log_success "Comprehensive seed data added successfully"
        
        # Display comprehensive summary
        log_info "Displaying comprehensive seed data summary..."
        docker compose -f $COMPOSE_FILE exec -T postgres psql -U postgres -d betting_championship << 'EOF'
-- Comprehensive data summary
SELECT 
    'sports' as table_name, 
    count(*) as records,
    string_agg(name, ', ') as sample_data
FROM sports
UNION ALL
SELECT 
    'teams', 
    count(*),
    CASE 
        WHEN count(*) <= 5 THEN string_agg(name, ', ' ORDER BY name)
        ELSE string_agg(name, ', ' ORDER BY name) FILTER (WHERE name IN (SELECT name FROM teams ORDER BY name LIMIT 5)) || ' (+' || (count(*) - 5)::text || ' more)'
    END
FROM teams  
UNION ALL
SELECT 
    'users', 
    count(*),
    string_agg(username, ', ')
FROM users
UNION ALL
SELECT 
    'seasons', 
    count(*),
    string_agg(name, ', ')
FROM seasons
UNION ALL
SELECT 
    'competitions', 
    count(*),
    string_agg(name, ', ')
FROM competitions
UNION ALL
SELECT 
    'matches', 
    count(*),
    CASE WHEN count(*) > 0 THEN count(*)::text || ' matches loaded' ELSE 'No matches' END
FROM matches
UNION ALL
SELECT 
    'players', 
    count(*),
    CASE WHEN count(*) > 0 THEN count(*)::text || ' players loaded' ELSE 'No players' END
FROM players
ORDER BY table_name;

-- Show some sample data
\echo 'Sample Teams:'
SELECT name, country FROM teams ORDER BY name LIMIT 10;

\echo 'Competition Details:'
SELECT name, format_type, status, start_date, end_date FROM competitions;
EOF
        
    else
        log_error "Failed to add comprehensive seed data"
        log_info "Falling back to basic seed data..."
        
        # Fallback to basic SQL seed data
        docker compose -f $COMPOSE_FILE exec -T postgres psql -U postgres -d betting_championship << 'EOF'
-- Basic fallback seed data
INSERT INTO sports (id, name, slug, description, category, is_active, popularity_score, rules, created_at, updated_at)
VALUES (gen_random_uuid(), 'Football', 'football', 'Association Football (Soccer)', 'team_sport', true, 95, '{"players_per_team": 11, "match_duration": 90}', NOW(), NOW())
ON CONFLICT (slug) DO NOTHING;

WITH sport_id AS (SELECT id FROM sports WHERE slug = 'football' LIMIT 1)
INSERT INTO seasons (id, name, slug, sport_id, year, start_date, end_date, is_current, status, prize_pool_total, created_at, updated_at)
VALUES (gen_random_uuid(), '2022 FIFA World Cup', 'fifa-world-cup-2022', (SELECT id FROM sport_id), 2022, '2022-11-20', '2022-12-18', false, 'completed', 440000000.00, NOW(), NOW())
ON CONFLICT (slug) DO NOTHING;

WITH sport_id AS (SELECT id FROM sports WHERE slug = 'football' LIMIT 1)
INSERT INTO teams (id, name, slug, short_name, sport_id, country, city, founded_year, is_active, max_players, created_at, updated_at)
SELECT gen_random_uuid(), 'Argentina', 'argentina', 'ARG', sport_id.id, 'Argentina', 'Buenos Aires', 1901, true, 25, NOW(), NOW()
FROM sport_id WHERE NOT EXISTS (SELECT 1 FROM teams WHERE slug = 'argentina')
UNION ALL
SELECT gen_random_uuid(), 'France', 'france', 'FRA', sport_id.id, 'France', 'Paris', 1904, true, 25, NOW(), NOW()
FROM sport_id WHERE NOT EXISTS (SELECT 1 FROM teams WHERE slug = 'france');

SELECT 'Basic seed data added' as status;
EOF
        
        if [ $? -eq 0 ]; then
            log_success "Basic seed data added as fallback"
        else
            log_error "Failed to add even basic seed data"
            return 1
        fi
    fi
}

# Function to verify deployment
verify_deployment() {
    log_info "Verifying deployment..."
    
    # Test API endpoints
    log_info "Testing API endpoints..."
    
    # Test health/docs endpoint
    if curl -s http://localhost:8000/docs > /dev/null; then
        log_success "✅ API Documentation accessible"
    else
        log_error "❌ API Documentation not accessible"
        exit 1
    fi
    
    # Test matches endpoint
    matches_response=$(curl -s http://localhost:8000/api/v1/matches/ || echo "failed")
    if [[ $matches_response == *"["* ]]; then
        log_success "✅ Matches endpoint working"
    else
        log_error "❌ Matches endpoint failed"
        exit 1
    fi
    
    # Test sports endpoint (with redirect)
    sports_response=$(curl -s -L http://localhost:8000/api/v1/sports/ || echo "failed")
    if [[ $sports_response == *"["* ]]; then
        log_success "✅ Sports endpoint working"
    else
        log_error "❌ Sports endpoint failed"
        exit 1
    fi
    
    log_success "All API endpoints verified"
}

# Function to display deployment summary
display_summary() {
    echo ""
    echo "🎉 DEPLOYMENT COMPLETE!"
    echo "======================"
    echo ""
    echo "📊 Services Status:"
    docker compose -f $COMPOSE_FILE ps
    echo ""
    echo "🌐 Service URLs:"
    echo "  • API Server:         http://localhost:8000"
    echo "  • API Documentation:  http://localhost:8000/docs"
    echo "  • Database (Adminer): http://localhost:8080"
    echo "  • Keycloak Auth:      http://localhost:8090"
    echo ""
    echo "🔑 Test Credentials:"
    echo "  • Admin User:    admin@bettingplatform.com / password123"
    echo "  • Test User:     test@example.com / password123"
    echo ""
    echo "🏆 FIFA World Cup 2022 Dataset:"
    echo "  • Complete 32-team tournament data"
    echo "  • All group stage and knockout matches"
    echo "  • Player rosters for all teams"
    echo "  • Historical match results"
    echo "  • Sample betting data and user groups"
    echo ""
    echo "📋 Database Connection:"
    echo "  • Host: localhost:5432"
    echo "  • Database: betting_championship"
    echo "  • Username: postgres"
    echo "  • Password: postgres123"
    echo ""
    echo "🧪 Ready for Postman Testing!"
    echo "  1. Import collection: docs/Betting_League_Championship_API.postman_collection.json"
    echo "  2. Import environment: docs/Betting_League_Championship_Development.postman_environment.json"
    echo "  3. Select 'Development' environment"
    echo "  4. Start testing with Authentication → Register User"
    echo ""
    echo "📝 Logs: docker compose -f $COMPOSE_FILE logs -f [service_name]"
    echo "🛑 Stop:  docker compose -f $COMPOSE_FILE down"
    echo ""
}

# Main deployment process
main() {
    echo "Starting professional development environment deployment..."
    echo ""
    
    # Check prerequisites
    check_docker
    
    # Deployment steps
    cleanup_environment
    start_services
    wait_for_services
    create_tables_and_seed
    verify_deployment
    
    # Display results
    display_summary
    
    log_success "Professional development environment ready! 🚀"
}

# Execute main function
main "$@"