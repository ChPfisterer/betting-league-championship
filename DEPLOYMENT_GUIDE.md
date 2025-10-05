# 🚀 Professional Development Environment

This guide provides a complete professional development environment setup for the Betting League Championship platform.

## 📋 Prerequisites

- **Docker Desktop** installed and running
- **Git** for version control
- **Postman** for API testing (optional but recommended)
- **At least 4GB RAM** available for containers

## ⚡ Quick Start

### One-Command Deployment

```bash
./deploy-dev.sh
```

This script will:
1. ✅ Clean up any existing environment
2. 🏗️ Build and start all services
3. 🗄️ Create database tables
4. 🌱 Add seed data
5. 🧪 Verify all endpoints
6. 📊 Display deployment summary

### Manual Step-by-Step (Alternative)

If you prefer to run steps manually:

```bash
# 1. Clean up existing environment
docker compose -f docker-compose.dev.yml down -v

# 2. Start services
docker compose -f docker-compose.dev.yml up --build -d

# 3. Wait for services (check with docker compose -f docker-compose.dev.yml ps)

# 4. Create tables (after backend is healthy)
docker compose -f docker-compose.dev.yml exec backend python -c "
import sys; sys.path.append('/app/src')
from models import *
from database import Base, engine
Base.metadata.create_all(bind=engine)
"

# 5. Add seed data
docker compose -f docker-compose.dev.yml exec postgres psql -U postgres -d betting_championship -f /path/to/seed.sql
```

## 🌐 Service URLs

| Service | URL | Description |
|---------|-----|-------------|
| **API Server** | http://localhost:8000 | Main FastAPI backend |
| **API Documentation** | http://localhost:8000/docs | Interactive API docs (Swagger UI) |
| **Database Admin** | http://localhost:8080 | Adminer database interface |
| **Auth Server** | http://localhost:8090 | Keycloak authentication |

## 🔐 Default Credentials

### Database
- **Host**: localhost:5432
- **Database**: betting_championship
- **Username**: postgres
- **Password**: postgres123

### Test Users
- **Admin**: admin@bettingplatform.com / password123
- **User**: test@example.com / password123

### Keycloak Admin
- **Username**: admin
- **Password**: admin123

## 📊 Seed Data Overview

The deployment includes:
- ⚽ **Sports**: Football (Soccer)
- 🏆 **Season**: 2022 FIFA World Cup
- 🇦🇷🇫🇷 **Teams**: Argentina, France
- 👥 **Users**: Admin and test users
- 🎯 **Competition**: FIFA World Cup 2022 Final
- ⚽ **Match**: Argentina vs France (Final result: 4-2)

## 🧪 API Testing with Postman

### Import Collections
1. **Collection**: `docs/Betting_League_Championship_API.postman_collection.json`
2. **Environment**: `docs/Betting_League_Championship_Development.postman_environment.json`

### Testing Flow
1. **Select Environment**: Choose "Betting League Championship - Development"
2. **Register User**: `Authentication → Register User`
3. **Login**: `Authentication → Login` (saves JWT token automatically)
4. **Test Endpoints**: Use saved token for protected endpoints

### Key Endpoints to Test
```bash
# Public endpoints
GET /api/v1/matches/        # List matches
GET /api/v1/sports/         # List sports  
GET /api/v1/teams/          # List teams

# Authentication
POST /api/v1/auth/register  # Register new user
POST /api/v1/auth/login     # Login user

# Protected endpoints (require JWT)
GET /api/v1/users/          # List users (admin only)
POST /api/v1/bets/          # Place bet
GET /api/v1/groups/         # List groups
```

## 🔧 Development Commands

### View Logs
```bash
# All services
docker compose -f docker-compose.dev.yml logs -f

# Specific service
docker compose -f docker-compose.dev.yml logs -f backend
docker compose -f docker-compose.dev.yml logs -f postgres
```

### Database Management
```bash
# Connect to database
docker compose -f docker-compose.dev.yml exec postgres psql -U postgres -d betting_championship

# View tables
\dt

# Check specific table
SELECT * FROM matches LIMIT 5;
```

### Service Management
```bash
# Stop services
docker compose -f docker-compose.dev.yml down

# Restart specific service
docker compose -f docker-compose.dev.yml restart backend

# Rebuild and restart
docker compose -f docker-compose.dev.yml up --build -d backend
```

## 🚨 Troubleshooting

### Port Conflicts
If ports are already in use:
```bash
# Check what's using ports
lsof -i :8000  # Backend
lsof -i :5432  # PostgreSQL
lsof -i :8080  # Adminer
lsof -i :8090  # Keycloak

# Kill processes or change ports in docker-compose.dev.yml
```

### Database Issues
```bash
# Reset database completely
docker compose -f docker-compose.dev.yml down -v
./deploy-dev.sh

# Check database connectivity
docker compose -f docker-compose.dev.yml exec postgres pg_isready -U postgres
```

### API Not Responding
```bash
# Check backend logs
docker compose -f docker-compose.dev.yml logs backend

# Check if backend is healthy
docker compose -f docker-compose.dev.yml ps backend

# Restart backend
docker compose -f docker-compose.dev.yml restart backend
```

## 📈 Health Checks

### Automated Verification
The deployment script automatically tests:
- ✅ Docker connectivity
- ✅ PostgreSQL health
- ✅ Backend API health
- ✅ Database tables creation
- ✅ Seed data insertion
- ✅ API endpoint responses

### Manual Health Check
```bash
# API health
curl http://localhost:8000/docs

# Database health  
docker compose -f docker-compose.dev.yml exec postgres pg_isready -U postgres

# Check seed data
curl http://localhost:8000/api/v1/matches/
```

## 🎯 Professional Features

### Environment Isolation
- ✅ Dedicated development database
- ✅ Isolated container network
- ✅ Volume persistence for data
- ✅ Hot-reload for development

### Data Integrity
- ✅ Proper enum validation
- ✅ Foreign key constraints
- ✅ Required field validation
- ✅ Seed data consistency

### Testing Ready
- ✅ Postman collections included
- ✅ Sample test data
- ✅ Authentication flow
- ✅ Comprehensive API coverage

### Production Preparation
- ✅ Health checks configured
- ✅ Logging structured
- ✅ Environment variables
- ✅ Security best practices

---

## 🎉 Success Criteria

Your environment is ready when:
1. **All services show "healthy" status**
2. **API documentation accessible at http://localhost:8000/docs**
3. **Matches endpoint returns data**: `curl http://localhost:8000/api/v1/matches/`
4. **Postman can authenticate and access protected endpoints**

**Ready to develop and test! 🚀**