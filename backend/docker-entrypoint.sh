#!/bin/bash
set -e

echo "🚀 Starting Backend Development Environment..."

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
while ! pg_isready -h postgres -p 5432 -U postgres; do
    echo "🔄 PostgreSQL is unavailable - sleeping"
    sleep 1
done
echo "✅ PostgreSQL is ready!"

# Run database migrations
echo "🏗️  Running database migrations..."
cd /app
python -m alembic upgrade head || {
    echo "❌ Migration failed, but continuing..."
}

# Create tables if they don't exist
echo "🏗️  Creating database tables..."
python create_tables.py || {
    echo "❌ Table creation failed, but continuing..."
}

# Run data seeding
echo "🌱 Seeding database with FIFA World Cup 2022 data..."
python FINAL_complete_world_cup_seeder.py || {
    echo "⚠️  Data seeding failed, but continuing with empty database..."
}

echo "✅ Backend initialization complete!"

# Start the FastAPI application
echo "🚀 Starting FastAPI server..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload