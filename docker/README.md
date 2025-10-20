# Docker Configuration

This directory contains Docker configurations for the Django-PostgreSQL application.

## Structure

```
docker/
├── web/
│   ├── Dockerfile          # Django web application container
│   └── requirements.txt    # Python dependencies
├── db/
│   ├── Dockerfile          # PostgreSQL database container
│   ├── init.sql           # Database initialization script
│   └── postgresql.conf    # PostgreSQL configuration
├── build.sh               # Build script for Docker images
├── test.sh                # Test script for containers
└── README.md              # This file
```

## Quick Start

### Local Development

1. **Build images:**
   ```bash
   ./docker/build.sh
   ```

2. **Start development environment:**
   ```bash
   docker-compose -f docker-compose.dev.yml up
   ```

3. **Access the application:**
   - Web app: http://localhost:8000
   - Database: localhost:5432

### Production (Docker Swarm)

1. **Initialize Swarm (if not already done):**
   ```bash
   docker swarm init
   ```

2. **Deploy stack:**
   ```bash
   docker stack deploy -c docker-compose.yml myapp
   ```

3. **Check services:**
   ```bash
   docker service ls
   docker service logs myapp_web
   ```

## Images

### Web Image (django-app:latest)
- Based on Python 3.11 slim
- Includes Django application and dependencies
- Runs with Gunicorn WSGI server
- Non-root user for security
- Health checks enabled

### Database Image (postgres-app:latest)
- Based on PostgreSQL 13
- Includes initialization scripts
- Custom configuration for performance
- Health checks enabled

## Environment Variables

### Web Service
- `DEBUG`: Enable/disable debug mode (default: False)
- `DB_HOST`: Database host (default: db)
- `DB_NAME`: Database name (default: postgres)
- `DB_USER`: Database user (default: postgres)
- `DB_PASSWORD`: Database password (default: postgres)
- `DB_PORT`: Database port (default: 5432)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### Database Service
- `POSTGRES_DB`: Database name (default: postgres)
- `POSTGRES_USER`: Database user (default: postgres)
- `POSTGRES_PASSWORD`: Database password (default: postgres)

## Networking

- **Development**: Bridge network for local testing
- **Production**: Overlay network for Swarm deployment
- Services communicate using service names (web → db)

## Volumes

- `db-data`: Persistent storage for PostgreSQL data
- Survives container restarts and updates

## Health Checks

Both services include health checks:
- **Web**: HTTP check on /login/ endpoint
- **Database**: PostgreSQL ready check

## Security Features

- Non-root users in containers
- Minimal base images
- No unnecessary packages
- Environment-based configuration
- Resource limits in production

## Scaling

The web service is configured to run with 2 replicas by default. To scale:

```bash
# Scale web service to 3 replicas
docker service scale myapp_web=3

# Scale down to 1 replica
docker service scale myapp_web=1
```

## Troubleshooting

### Check service status
```bash
docker service ls
docker service ps myapp_web
docker service ps myapp_db
```

### View logs
```bash
docker service logs myapp_web
docker service logs myapp_db
```

### Access container shell
```bash
# Development
docker-compose -f docker-compose.dev.yml exec web bash
docker-compose -f docker-compose.dev.yml exec db bash

# Production (find container ID first)
docker ps
docker exec -it <container_id> bash
```

### Database access
```bash
# Development
docker-compose -f docker-compose.dev.yml exec db psql -U postgres -d postgres

# Production
docker exec -it <db_container_id> psql -U postgres -d postgres
```