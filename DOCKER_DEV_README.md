# Docker Development Environment

## 🚀 Quick Start

The development environment includes:
- **PostgreSQL 17.6** - Main database + Keycloak database
- **FastAPI Backend** - API server with hot reload
- **Keycloak 26.3.2** - Authentication server with pre-configured realm
- **Adminer** - Database management UI

### Prerequisites
- Docker & Docker Compose installed
- 8GB+ RAM recommended
- Ports 8000, 8080, 8090, 5432 available

### Start Development Environment

```bash
# Clone and navigate to project
git clone <repository-url>
cd betting-league-championship

# Start all services
docker compose -f docker-compose.dev.yml --env-file .env.dev up --build -d

# Check service status
docker compose -f docker-compose.dev.yml ps

# View logs
docker compose -f docker-compose.dev.yml logs -f backend
```

---

## 🌐 Service URLs

| Service | URL | Credentials |
|---------|-----|-------------|
| **Backend API** | http://localhost:8000 | JWT Token |
| **API Docs** | http://localhost:8000/docs | - |
| **Keycloak Admin** | http://localhost:8090 | admin / admin123 |
| **Keycloak Realm** | http://localhost:8090/realms/betting-platform | - |
| **Adminer (DB)** | http://localhost:8080 | postgres / postgres123 |
| **PostgreSQL** | localhost:5432 | postgres / postgres123 |

---

## 🔐 Pre-configured Test Users

The Keycloak realm comes with test users:

| Username | Password | Role | Email |
|----------|----------|------|-------|
| **admin** | admin123 | super_admin, admin | admin@bettingleague.com |
| **moderator** | mod123 | moderator, user | moderator@bettingleague.com |
| **testuser** | test123 | user | test@bettingleague.com |

### Authentication Flow

```bash
# Test authentication with curl
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "test123"
  }'
```

---

## 🗄️ Database Access

### Via Adminer (Web UI)
1. Go to http://localhost:8080
2. Server: `postgres`
3. Username: `postgres`
4. Password: `postgres123`
5. Database: `betting_championship`

### Via Command Line
```bash
# Connect to PostgreSQL container
docker compose -f docker-compose.dev.yml exec postgres psql -U postgres -d betting_championship

# List tables
\dt

# Check database status
SELECT 'Database is ready!' as status;
```

### Database Structure
- **Main DB**: `betting_championship` - API data
- **Keycloak DB**: `keycloak` - Authentication data
- **Extensions**: uuid-ossp, pgcrypto

---

## 🧪 Testing the API

### Health Check
```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy", "timestamp": "...", "version": "1.0.0"}
```

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Using Postman
1. Import collection: `docs/Betting_League_Championship_API.postman_collection.json`
2. Import environment: `docs/Betting_League_Championship_Development.postman_environment.json`
3. Update base_url to `http://localhost:8000`
4. Run authentication flow to get JWT tokens

---

## 🔧 Development Workflow

### File Changes & Hot Reload
The backend container has hot reload enabled:
```bash
# Backend files are mounted as read-only
# Changes in ./backend/ trigger automatic reload
# Check logs: docker compose -f docker-compose.dev.yml logs -f backend
```

### Database Migrations
```bash
# Run migrations inside backend container
docker compose -f docker-compose.dev.yml exec backend alembic upgrade head

# Create new migration
docker compose -f docker-compose.dev.yml exec backend alembic revision --autogenerate -m "description"
```

### Running Tests
```bash
# Run all tests
docker compose -f docker-compose.dev.yml exec backend pytest

# Run with coverage
docker compose -f docker-compose.dev.yml exec backend pytest --cov=src --cov-report=html

# Run specific tests
docker compose -f docker-compose.dev.yml exec backend pytest tests/api/
```

---

## 🔍 Monitoring & Debugging

### Service Health Status
```bash
# Check all services
docker compose -f docker-compose.dev.yml ps

# Check specific service health
curl http://localhost:8000/health        # Backend
curl http://localhost:8090/health/ready  # Keycloak
```

### Logs
```bash
# All services
docker compose -f docker-compose.dev.yml logs

# Specific service
docker compose -f docker-compose.dev.yml logs -f backend
docker compose -f docker-compose.dev.yml logs -f keycloak
docker compose -f docker-compose.dev.yml logs -f postgres

# Last 100 lines
docker compose -f docker-compose.dev.yml logs --tail=100 backend
```

### Debug Backend Container
```bash
# Enter backend container
docker compose -f docker-compose.dev.yml exec backend bash

# Check Python environment
docker compose -f docker-compose.dev.yml exec backend python --version
docker compose -f docker-compose.dev.yml exec backend pip list

# Check application structure
docker compose -f docker-compose.dev.yml exec backend ls -la /app
```

---

## 🛠️ Troubleshooting

### Port Conflicts
```bash
# Check what's using ports
lsof -i :8000  # Backend
lsof -i :8080  # Adminer
lsof -i :8090  # Keycloak
lsof -i :5432  # PostgreSQL

# Stop conflicting services or change ports in .env.dev
```

### Database Connection Issues
```bash
# Check PostgreSQL logs
docker compose -f docker-compose.dev.yml logs postgres

# Test database connection
docker compose -f docker-compose.dev.yml exec postgres pg_isready -U postgres

# Reset database (WARNING: destroys data)
docker compose -f docker-compose.dev.yml down -v
docker compose -f docker-compose.dev.yml up --build -d
```

### Keycloak Issues
```bash
# Check Keycloak startup
docker compose -f docker-compose.dev.yml logs keycloak

# Reset Keycloak realm import
docker compose -f docker-compose.dev.yml restart keycloak

# Access Keycloak admin directly
# http://localhost:8090/admin (admin/admin123)
```

### Backend Build Issues
```bash
# Rebuild backend container
docker compose -f docker-compose.dev.yml build --no-cache backend

# Check Dockerfile
cat backend/docker/Dockerfile.dev

# Clean Docker cache
docker system prune -a
```

---

## ⚙️ Configuration

### Environment Variables (.env.dev)
```bash
# Copy example and modify
cp .env.dev.example .env.dev

# Key settings
POSTGRES_PASSWORD=postgres123      # Database password
KEYCLOAK_ADMIN_PASSWORD=admin123   # Keycloak admin password
SECRET_KEY=dev-secret-key         # JWT signing key
LOG_LEVEL=DEBUG                   # Logging level
```

### Custom Ports
Edit `.env.dev`:
```bash
BACKEND_PORT=8001      # Change backend port
KEYCLOAK_PORT=8091     # Change Keycloak port
ADMINER_PORT=8081      # Change Adminer port
POSTGRES_PORT=5433     # Change PostgreSQL port
```

### Performance Tuning
```bash
# Increase PostgreSQL shared_buffers
# Add to docker-compose.dev.yml postgres service:
command: postgres -c shared_buffers=256MB -c max_connections=200

# Allocate more memory to containers
# Add to services:
deploy:
  resources:
    limits:
      memory: 2G
```

---

## 🚀 Production Deployment

This development setup is NOT for production. For production:

1. Use `docker-compose.base.yml` with production overrides
2. Enable TLS/SSL certificates
3. Use external PostgreSQL with backups
4. Configure proper Keycloak realm with security
5. Set strong passwords and secrets
6. Enable monitoring and logging
7. Configure load balancing and scaling

---

## 📚 Additional Resources

- **API Documentation**: `docs/DEVELOPER_MANUAL.md`
- **Postman Collection**: `docs/POSTMAN_README.md`
- **Backend Structure**: `backend/README.md`
- **Production Setup**: `infrastructure/docker/README.md`

---

## 🆘 Getting Help

### Common Commands
```bash
# Full reset (destroys all data)
docker compose -f docker-compose.dev.yml down -v
docker compose -f docker-compose.dev.yml up --build -d

# Update services
docker compose -f docker-compose.dev.yml pull
docker compose -f docker-compose.dev.yml up --build -d

# Stop all services
docker compose -f docker-compose.dev.yml down

# Stop and remove all data
docker compose -f docker-compose.dev.yml down -v
```

### Support
- Check logs first: `docker compose -f docker-compose.dev.yml logs [service]`
- Verify service health: `docker compose -f docker-compose.dev.yml ps`
- Review documentation: `docs/DEVELOPER_MANUAL.md`
- GitHub Issues: Report bugs and ask questions

---

**Happy Development! 🎉**