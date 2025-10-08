# 🚀 Development Environment Scripts

This directory contains scripts to easily start and manage the Betting League Championship development environment.

## 📋 Prerequisites

- Docker and Docker Compose
- Node.js v22.20.0+ (managed via nvm)
- Git

## 🎯 Quick Start

### Full Development Environment (Recommended)
```bash
# Start everything (backend + frontend)
./start-dev-full.sh
```

This script will:
- ✅ Check Docker and Node.js setup
- 🐳 Start all backend services (PostgreSQL, Keycloak, FastAPI, Adminer)
- 📱 Start Angular frontend development server
- 🎯 Wait for all services to be healthy
- 📊 Display service URLs and helpful information

### Backend Services Only
```bash
# Start only backend services
./start-backend.sh
```

Use this when you want to:
- Work on frontend in a separate terminal
- Use different frontend development tools
- Debug frontend issues independently

### Frontend Only
```bash
# Start only frontend (requires backend to be running)
./start-frontend.sh
```

Use this when you want to:
- Backend services are already running
- Restart just the frontend during development
- Work on frontend-only changes

### Stop All Services
```bash
# Stop everything
./stop-dev.sh
```

## 🌐 Service URLs

When running, the following services will be available:

| Service | URL | Description |
|---------|-----|-------------|
| 📱 **Frontend** | http://localhost:4200 | Angular development server |
| 🚀 **Backend API** | http://localhost:8000 | FastAPI application |
| 📊 **API Documentation** | http://localhost:8000/docs | Interactive API docs (Swagger) |
| 🔐 **Keycloak** | http://localhost:8080 | Authentication server |
| 💾 **Adminer** | http://localhost:8081 | Database management |
| 🐘 **PostgreSQL** | localhost:5432 | Database server |

## 🛠️ Development Workflow

### Typical Development Session
```bash
# 1. Start full environment
./start-dev-full.sh

# 2. Open your browser to http://localhost:4200
# 3. Make changes to code (auto-reload enabled)
# 4. Use Ctrl+C to stop when done
```

### Frontend Only Development
```bash
# 1. Start backend services
./start-backend.sh

# 2. In another terminal, start frontend
cd frontend/betting-league-app
./start-dev.sh

# 3. Stop backend when done
./stop-dev.sh
```

## 🐛 Troubleshooting

### Services Won't Start
```bash
# Check Docker status
docker --version
docker compose version

# Check for port conflicts
lsof -i :4200  # Frontend
lsof -i :8000  # Backend
lsof -i :8080  # Keycloak
lsof -i :5432  # PostgreSQL
```

### Node.js Version Issues
```bash
# Install correct Node.js version
nvm install 22.20.0
nvm use 22.20.0
nvm alias default 22.20.0
```

### Docker Issues
```bash
# Clean up Docker resources
./stop-dev.sh
docker system prune -f

# Restart Docker and try again
./start-dev-full.sh
```

### Frontend Build Errors
```bash
# Clear npm cache and reinstall
cd frontend/betting-league-app
rm -rf node_modules package-lock.json
npm install
```

## 📁 Script Details

### `start-dev-full.sh`
- **Purpose**: Complete development environment setup
- **What it does**:
  - Validates Docker and Node.js setup
  - Stops any existing services
  - Starts backend services via Docker Compose
  - Waits for services to be healthy
  - Starts Angular frontend development server
  - Displays status and helpful information
- **Signal handling**: Ctrl+C gracefully stops all services

### `start-backend.sh`
- **Purpose**: Backend services only
- **What it does**:
  - Starts Docker Compose services
  - Shows service status
  - Provides connection information
- **Use case**: When developing frontend separately

### `stop-dev.sh`
- **Purpose**: Clean shutdown of all services
- **What it does**:
  - Kills frontend development servers
  - Stops Docker services
  - Optionally cleans up Docker volumes/networks

### `frontend/betting-league-app/start-dev.sh`
- **Purpose**: Frontend development server only
- **What it does**:
  - Sets up correct Node.js version via nvm
  - Starts Angular development server
- **Use case**: Frontend-only development

## 🎛️ Environment Configuration

The development environment uses:
- **Database**: PostgreSQL with persistent data
- **Authentication**: Keycloak with dev realm configuration
- **Backend**: FastAPI with hot reload
- **Frontend**: Angular with live reload
- **Database UI**: Adminer for database management

## 🔧 Customization

### Modify Docker Services
Edit `docker-compose.dev.yml` to:
- Change port mappings
- Add new services
- Modify environment variables

### Modify Frontend Configuration
Edit `frontend/betting-league-app/src/environments/environment.ts` to:
- Change API endpoints
- Modify Keycloak configuration
- Update feature flags

## 📚 Additional Resources

- [Project Documentation](../docs/)
- [API Documentation](http://localhost:8000/docs) (when running)
- [Frontend Guide](../frontend/README.md)
- [Backend Guide](../backend/README.md)

## 🆘 Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Review service logs: `docker compose -f docker-compose.dev.yml logs`
3. Check the project documentation
4. Open an issue with detailed error information